#!/usr/bin/env python3
"""Habille un clip généré : mise au format 1080×1920, bandeau, sous-titres, voix off et mixage.

    python3 engine/finish_clip.py clips/escargot.json source.mp4

Le fichier JSON décrit le bandeau, les répliques (texte affiché, texte lu, instant de départ)
et, si besoin, la coupe à garder dans le clip source.
"""
import html
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # voix, synthèse des sons et table de mixage du générateur de quiz

ROOT, OUT, SR = build.ROOT, build.OUT, build.SR


def run(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=True, cwd=ROOT, **kw)


def village_ambience(dur):
    """Fond sonore discret pour un clip muet : souffle de vent, quelques oiseaux, une cloche au loin."""
    rng = np.random.default_rng(7)
    n = int(dur * SR)
    t = np.arange(n) / SR
    wind = build.filt(rng.standard_normal(n), "lowpass", 500) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.13 * t + 1.0))
    bed = build.Mix(dur)
    bed.buf[:n] += (wind / np.abs(wind).max() * 0.035)[:, None]
    for _ in range(int(dur * 0.9)):                       # gazouillis : petites notes aiguës qui glissent
        at, base = rng.uniform(0.5, dur - 1.0), rng.uniform(2800, 4600)
        for k in range(rng.integers(2, 5)):
            tt = build.axis(0.09)
            f = base * (1 + 0.25 * np.sin(2 * np.pi * rng.uniform(6, 14) * tt)) + rng.uniform(-300, 300)
            chirp = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / 0.09) ** 2
            bed.add(chirp, at + k * rng.uniform(0.10, 0.16), rng.uniform(0.012, 0.03), pan=rng.uniform(-0.8, 0.8))
    if dur > 6:                                            # une cloche lointaine vers la fin
        bell = build.filt(build.bell(392.0, 3.0, 0.9), "lowpass", 1500)
        bed.add(bell, dur - 3.4, 0.045, pan=-0.3)
    return bed.buf


def main():
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    src = Path(sys.argv[2]).resolve()
    work = OUT / cfg["id"]
    work.mkdir(parents=True, exist_ok=True)
    start, end = cfg.get("trim", [0, None])
    probe = json.loads(run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type", "-of", "json", src],
                           capture_output=True, text=True).stdout)
    end = float(probe["format"]["duration"]) if end is None else end
    dur = end - start
    has_audio = any(s["codec_type"] == "audio" for s in probe["streams"])

    # --- calques : bandeau permanent, un sous-titre par réplique
    lines = cfg["lines"]
    voices = [build.tts(l["say"], l.get("speed", 1.0)) for l in lines]
    layout = cfg.get("layout", {})
    top = layout.get("banner_top", 1196)          # haut du bandeau, en pixels sur 1920
    cap = layout.get("caption_top")               # haut des sous-titres ; par défaut juste au-dessus du bandeau
    cap_style = f' style="top:{cap}px;bottom:auto"' if cap is not None else ""
    jobs = [{"out": str(work / "bandeau.png"),
             "html": f'<div class="tag anton" style="top:{top}px">{html.escape(cfg["banner"]["tag"])}</div>'
                     f'<div class="title anton" style="top:{top + 86}px">{html.escape(cfg["banner"]["title"])}</div>'}]
    for i, l in enumerate(lines):
        jobs.append({"out": str(work / f"cap{i}.png"), "html": f'<div class="cap"{cap_style}><span>{html.escape(l["text"])}</span></div>'})
    run(["node", "engine/overlay.mjs"], input=json.dumps(jobs), text=True)

    # --- son : ambiance d'origine sous la voix, petit carillon d'ouverture
    mix = build.Mix(dur)
    n = int(dur * SR)
    if has_audio:
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", start, "-t", dur, "-i", src, "-vn", "-ac", "2", "-ar", SR, work / "ambiance.wav"])
        amb, _ = sf.read(work / "ambiance.wav", dtype="float64")
        amb = amb[:n] / max(1e-6, np.abs(amb).max()) * 0.5
        duck = np.ones(len(amb))
        for l, v in zip(lines, voices):
            a, b = int(l["at"] * SR), int((l["at"] + len(v) / SR + 0.15) * SR)
            duck[max(0, a - 2400):b] = 0.35
        k = int(0.08 * SR)
        duck = np.convolve(duck, np.ones(k) / k, mode="same")
        mix.buf[:len(amb)] += amb * duck[:, None]
    else:
        mix.buf[:n] += village_ambience(dur)[:n]
    if cfg.get("chime", True):
        for f, at in ((880.0, 0.0), (1174.66, 0.14)):
            mix.add(build.bell(f, 0.9, 0.22), at, 0.16)
    for l, v in zip(lines, voices):
        mix.add(v, l["at"], 0.95)
    audio = mix.buf[:n]
    fade = int(0.2 * SR)
    audio[-fade:] *= np.linspace(1, 0, fade)[:, None]
    import pyloudnorm
    audio = audio * 10 ** ((-14.0 - pyloudnorm.Meter(SR).integrated_loudness(audio)) / 20)
    sf.write(work / "audio.wav", np.tanh(audio / 0.84) * 0.84, SR, subtype="PCM_16")

    # --- image : cadrage 9:16 plein écran, puis calques
    zoom = cfg.get("zoom", 1.0)
    chain = [f"[0:v]scale={int(1080 * zoom)}:{int(1920 * zoom)}:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,unsharp=5:5:0.5[v0]",
             "[v0][1:v]overlay=0:0[v1]"]
    inputs = ["-ss", start, "-t", dur, "-i", src, "-i", work / "bandeau.png"]
    last = "v1"
    for i, (l, v) in enumerate(zip(lines, voices)):
        inputs += ["-i", work / f"cap{i}.png"]
        a, b = l["at"], l["at"] + len(v) / SR + 0.35
        chain.append(f"[{last}][{i + 2}:v]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[c{i}]")
        last = f"c{i}"
    final = OUT / f"{cfg['id']}.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", work / "audio.wav", "-filter_complex", ";".join(chain),
         "-map", f"[{last}]", "-map", f"{len(lines) + 2}:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
         "-r", "30", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", final])
    post = cfg.get("post", {})
    (OUT / f"{cfg['id']}-legende.txt").write_text(post.get("caption", "") + "\n\n" + " ".join("#" + h for h in post.get("hashtags", [])) + "\n", encoding="utf-8")
    for l, v in zip(lines, voices):
        print(f"  {l['at']:5.2f} s -> {l['at'] + len(v) / SR:5.2f} s  {l['text']}")
    print(f"Vidéo prête : {final}  ({dur:.1f} s)")


if __name__ == "__main__":
    main()
