#!/usr/bin/env python3
"""Fabrique une vidéo « Niveau 10 » (1080×1920) à partir d'un fichier d'épisode.

    python3 engine/build.py episodes/001-formes-pays.json
    python3 engine/build.py episodes/001-formes-pays.json --stills 0,1,8.5   (images de contrôle seulement)

Étapes : voix de synthèse -> timeline -> bande-son -> images -> assemblage.
"""
import argparse
import hashlib
import json
import math
import subprocess
import sys
import urllib.request
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, resample_poly, sosfilt

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache"
OUT = ROOT / "out"
SR = 48000
FPS = 30
BEAT = 0.5  # 120 bpm : toutes les durées sont des multiples d'un temps

# Couleur et intitulé de chaque niveau, du plus facile à l'impossible.
COLORS = ["#34E0A1", "#7BE66E", "#C3E64B", "#FFD43B", "#FFB536", "#FF9233", "#FF7A3D", "#FF4D5E", "#F23DB3", "#A855F7"]
LABELS = ["Échauffement", "Facile", "Facile", "Moyen", "Moyen", "Difficile", "Difficile", "Expert", "Légende", "Impossible"]

VOICE = "ff_siwis"
MODEL_URL = "https://huggingface.co/fastrtc/kokoro-onnx/resolve/main/"
rng = np.random.default_rng(10)


# ----------------------------------------------------------------------------- voix
_kokoro = None


def _model_file(name):
    path = CACHE / name
    if not path.exists():
        CACHE.mkdir(exist_ok=True)
        print(f"Téléchargement du modèle de voix : {name}")
        urllib.request.urlretrieve(MODEL_URL + name, path)
    return str(path)


def tts(text, speed=1.0):
    """Voix française (Kokoro, licence Apache 2.0). Renvoie un signal mono à 48 kHz."""
    global _kokoro
    key = hashlib.sha1(f"{VOICE}|{speed}|{text}".encode()).hexdigest()[:16]
    path = CACHE / "tts" / f"{key}.wav"
    if not path.exists():
        if _kokoro is None:
            from kokoro_onnx import Kokoro

            _kokoro = Kokoro(_model_file("kokoro-v1.0.onnx"), _model_file("voices-v1.0.bin"))
        samples, sr = _kokoro.create(text, voice=VOICE, speed=speed, lang="fr-fr")
        path.parent.mkdir(parents=True, exist_ok=True)
        sf.write(path, samples, sr)
    s, sr = sf.read(path, dtype="float32")
    s = resample_poly(s, SR, sr).astype(np.float64)
    loud = np.where(np.abs(s) > 0.02)[0]  # on retire les silences de début et de fin
    s = s[max(0, loud[0] - int(0.01 * SR)) : loud[-1] + int(0.06 * SR)]
    s = filt(s, "highpass", 75)
    return s / np.abs(s).max() * 0.9


# ----------------------------------------------------------------------------- synthèse des sons
def axis(d):
    return np.arange(int(d * SR)) / SR


def filt(x, kind, freq, order=2):
    return sosfilt(butter(order, freq, kind, fs=SR, output="sos"), x)


def tick(freq=1500.0):
    t = axis(0.07)
    s = np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.010) + 0.5 * np.sin(2 * np.pi * freq * 1.5 * t) * np.exp(-t / 0.006)
    click = 0.2 * rng.standard_normal(len(t)) * np.exp(-t / 0.0015)
    return (s + click) * np.minimum(1, t / 0.0005)


def boom(f0=120.0, f1=42.0, d=0.5, tau=0.12):
    t = axis(d)
    f = f1 + (f0 - f1) * np.exp(-t / 0.04)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / tau)
    click = filt(rng.standard_normal(len(t)), "lowpass", 1800) * np.exp(-t / 0.02) * 0.5
    return np.tanh(1.6 * (body + click))


def whoosh(d=0.36):
    n = rng.standard_normal(int(d * SR))
    k = np.linspace(0, 1, len(n))
    lo, hi = filt(n, "bandpass", [250, 1200]), filt(n, "bandpass", [1200, 6000])
    return (lo * (1 - k) + hi * k) * np.sin(np.pi * k) ** 1.5


def pop():
    t = axis(0.12)
    f = 520 + 600 * (t / 0.12)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.035)


def bell(freq, d=1.0, tau=0.28):
    t = axis(d)
    partials = [(1.0, 1.0, 1.0), (2.0, 0.45, 0.7), (3.01, 0.22, 0.5), (4.2, 0.12, 0.35)]
    s = sum(a * np.sin(2 * np.pi * freq * m * t) * np.exp(-t / (tau * k)) for m, a, k in partials)
    return s * np.minimum(1, t / 0.003)


def ding(root=987.77):
    """Bonne réponse : deux notes de cloche montantes (quarte)."""
    out = np.zeros(int(1.2 * SR))
    a, b = bell(root, 0.9), bell(root * 4 / 3, 1.0)
    out[: len(a)] += 0.8 * a
    off = int(0.09 * SR)
    out[off : off + len(b)] += b
    return out


def riser(d=1.0):
    t = axis(d)
    k = t / d
    tone = 0.5 * np.sin(2 * np.pi * np.cumsum(180 * np.power(2, 3.2 * k)) / SR)
    return (tone + 0.35 * filt(rng.standard_normal(len(t)), "highpass", 1500)) * k**2


def saw(freq, t, harmonics=10):
    s = np.zeros_like(t)
    for h in range(1, harmonics + 1):
        if freq * h < SR / 2:
            s += np.sin(2 * np.pi * freq * h * t) / h
    return 0.6 * s


def pluck(freq, d=0.3, tau=0.08):
    t = axis(d)
    return (np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t)) * np.exp(-t / tau) * np.minimum(1, t / 0.002)


class Mix:
    """Table de mixage stéréo : on pose chaque son à sa date."""

    def __init__(self, duration):
        self.buf = np.zeros((int(duration * SR) + SR, 2))

    def add(self, s, at, gain=1.0, pan=0.0):
        i = int(round(at * SR))
        if i < 0:
            s, i = s[-i:], 0
        s = s[: max(0, len(self.buf) - i)]
        left, right = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
        self.buf[i : i + len(s), 0] += s * gain * left * math.sqrt(2)
        self.buf[i : i + len(s), 1] += s * gain * right * math.sqrt(2)


# ----------------------------------------------------------------------------- timeline
def ceil_beat(x):
    return math.ceil(x / BEAT - 1e-9) * BEAT


def make_timeline(ep, assets, voices):
    n = len(ep["levels"])
    step = 0.16  # défilement des visuels pendant l'accroche
    intro_end = ceil_beat(max(voices["intro"] + 0.1, n * step + 1.4))
    tl = {
        "fps": FPS, "mode": ep["mode"], "prompt": ep["prompt"],
        "intro": {**{k: ep["intro"][k] for k in ("kicker", "lines", "accentLine", "teaser", "sub")}, "start": 0.0, "end": intro_end, "cycleStep": step},
        "levels": [],
    }
    t = intro_end
    for i, lv in enumerate(ep["levels"]):
        timer = lv.get("timer", 5)
        cd = t + BEAT              # début du compte à rebours
        rev = cd + timer           # révélation
        end = rev + 2.0
        tl["levels"].append({
            "n": i + 1, "start": t, "cd": cd, "hintAt": cd + ceil_beat(timer / 2), "rev": rev, "end": end, "timer": timer,
            "color": COLORS[i], "label": LABELS[i], "name": lv["name"], "hint": lv["hint"], "fact": lv["fact"],
            "question": lv.get("question"), "qsmall": lv.get("qsmall"), **assets["levels"][i],
        })
        t = end
    outro_end = ceil_beat(t + max(voices["outro"] + 0.9, 4.0))
    tl["outro"] = {**{k: ep["outro"][k] for k in ("lines", "accentLine", "cta", "cta2")}, "start": t, "end": outro_end}
    tl["duration"] = outro_end
    return tl


# ----------------------------------------------------------------------------- bande-son
def soundtrack(tl, voice):
    total = tl["duration"]
    L = tl["levels"]
    sfx, bed, vox = Mix(total), Mix(total), Mix(total)
    n_total = len(sfx.buf)

    def level_at(t):
        for lv in L:
            if lv["start"] <= t < lv["end"]:
                return lv["n"]
        return 0 if t < L[0]["start"] else 5  # intro : calme ; outro : moyen

    # --- voix
    vox.add(voice["intro"], 0.08)
    for lv, v in zip(L, voice["levels"]):
        vox.add(v, lv["rev"] + 0.3)
    vox.add(voice["outro"], tl["outro"]["start"] + 0.35)

    # --- accroche : impact, défilement, montée
    intro = tl["intro"]
    sfx.add(boom(140, 45, 0.6, 0.16), 0.0, 0.55)
    for i in range(len(L) - 1):
        sfx.add(tick(1100 + 110 * i), (i + 1) * intro["cycleStep"], 0.22, pan=(-1) ** i * 0.3)
    sfx.add(boom(110, 40, 0.5, 0.14), (len(L) - 1) * intro["cycleStep"] + 0.1, 0.45)
    sfx.add(riser(1.0), intro["end"] - 1.0, 0.16)

    # --- niveaux
    for lv in L:
        last = lv["n"] == len(L)
        sfx.add(whoosh(), lv["start"] - 0.06, 0.3, pan=0.0)
        sfx.add(boom(150 if last else 120, 38 if last else 45, 0.7 if last else 0.45, 0.2 if last else 0.11), lv["start"] + 0.1, 0.75 if last else 0.5)
        if last:
            sfx.add(riser(1.0), lv["start"] - 0.95, 0.24)
        for s in range(lv["timer"]):
            final = s == lv["timer"] - 1
            sfx.add(tick(1500), lv["cd"] + s, 0.4)
            if final:  # dernière seconde : le tic-tac s'emballe
                for q in (0.25, 0.5, 0.75):
                    sfx.add(tick(1500 + 500 * q), lv["cd"] + s + q, 0.3)
            else:
                sfx.add(tick(1050), lv["cd"] + s + 0.5, 0.16)
        sfx.add(pop(), lv["hintAt"], 0.3)
        sfx.add(ding(), lv["rev"], 0.36)
        sfx.add(boom(100, 50, 0.3, 0.08), lv["rev"], 0.4)

    # --- outro : montée des dix tuiles puis accord final
    o = tl["outro"]
    sfx.add(whoosh(), o["start"] - 0.06, 0.3)
    scale = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16]
    for i, semis in enumerate(scale):
        sfx.add(pluck(523.25 * 2 ** (semis / 12), 0.35, 0.09), o["start"] + 0.45 + i * 0.11, 0.2, pan=-0.5 + i / 9)
    for f in (440.0, 554.37, 659.25, 880.0):
        sfx.add(bell(f, 1.6, 0.5), o["start"] + 1.0, 0.11)

    # --- nappe musicale : basse pulsée, pied, charley, arpège (la tension monte avec le niveau)
    roots = [55.0, 55.0, 43.65, 49.0]            # la mineur : Am, Am, F, G
    arps = {                                     # arpège : uniquement des notes de l'accord en cours
        55.0: [220.0, 261.63, 329.63, 440.0, 523.25, 440.0, 329.63, 261.63],     # la mineur
        43.65: [174.61, 220.0, 261.63, 349.23, 440.0, 349.23, 261.63, 220.0],    # fa majeur
        49.0: [196.0, 246.94, 293.66, 392.0, 493.88, 392.0, 293.66, 246.94],     # sol majeur
    }
    start = tl["intro"]["end"]
    eighths = int((total - start) / (BEAT / 2))
    for e in range(eighths):
        t = start + e * BEAT / 2
        lvl = level_at(t)
        tension = 0.35 + 0.065 * lvl
        root = roots[int((t - start) / 2.0) % len(roots)]
        tt = axis(0.24)
        note = filt(saw(root * 2, tt) * np.exp(-tt / 0.11), "lowpass", 300 + 900 * tension)
        bed.add(note, t, 0.3 * tension)
        # motif médium (fondamentale / quinte) : la pulsation qu'on entend même sans graves
        bed.add(pluck(root * (4 if e % 2 == 0 else 6), 0.22, 0.05), t, 0.05 + 0.06 * tension, pan=-0.2 if e % 2 else 0.2)
        if e % 2 == 0:
            bed.add(boom(105, 46, 0.3, 0.07), t, 0.24 + 0.2 * tension)
        elif lvl >= 3:
            th = axis(0.05)
            bed.add(filt(rng.standard_normal(len(th)), "highpass", 7000) * np.exp(-th / 0.012), t, 0.07)
        if lvl >= 4:  # arpège : croches d'abord, doubles croches à partir du niveau 7, une octave plus haut au niveau 9
            for half in ((0, 1) if lvl >= 7 else (1,)):
                arp = arps[root]
                idx = (e * 2 + half) % len(arp)
                bed.add(pluck(arp[idx] * (2 if lvl >= 9 else 1), 0.3, 0.08), t + half * BEAT / 4, 0.08, pan=0.45 if (e * 2 + half) % 2 else -0.45)
    # nappe tenue, du début à la fin
    tp = axis(total)
    pad = np.zeros_like(tp)
    for bar in range(int(total / 2.0) + 1):
        root = roots[bar % len(roots)] if bar * 2.0 >= start else 55.0
        seg = (tp >= bar * 2.0 - 0.3) & (tp < bar * 2.0 + 2.3)
        ts = tp[seg] - (bar * 2.0 - 0.3)
        env = np.clip(ts / 0.3, 0, 1) * np.clip((2.6 - ts) / 0.3, 0, 1)
        chord = sum(np.sin(2 * np.pi * root * m * ts) for m in (2, 3, 4, 4.76 if root == 55.0 else 5))
        pad[seg] += chord * env
    bed.add(filt(pad, "lowpass", 900) * (1 + 0.15 * np.sin(2 * np.pi * 0.25 * tp)), 0.0, 0.035)

    # --- la musique s'efface sous la voix et au moment des réponses
    duck = np.ones(n_total)
    env = np.abs(vox.buf).max(axis=1)
    win = int(0.12 * SR)
    active = np.convolve((env > 0.02).astype(float), np.ones(win) / win, mode="same") > 0.05
    duck[active] = 0.42
    for lv in L:
        i = int(lv["rev"] * SR)
        duck[i : i + int(0.45 * SR)] = np.minimum(duck[i : i + int(0.45 * SR)], 0.3)
    smooth = int(0.08 * SR)
    duck = np.convolve(duck, np.ones(smooth) / smooth, mode="same")

    out = vox.buf * 0.95 + sfx.buf * 0.8 + bed.buf * duck[:, None] * 0.62
    out = out[: int(total * SR)]
    fade = int(0.25 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)[:, None]

    # --- niveau final : -14 LUFS, crêtes limitées
    import pyloudnorm

    loud = pyloudnorm.Meter(SR).integrated_loudness(out)
    out = out * 10 ** ((-14.0 - loud) / 20)
    return np.tanh(out / 0.84) * 0.84, loud


# ----------------------------------------------------------------------------- assemblage
def run(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=True, cwd=ROOT, **kw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--stills", help="instants (en secondes, séparés par des virgules) : n'écrit que des images de contrôle")
    ap.add_argument("--audio-only", action="store_true", help="refait la bande-son et réassemble, en gardant les images déjà rendues")
    args = ap.parse_args()

    ep = json.loads(Path(args.episode).read_text(encoding="utf-8"))
    work = OUT / ep["id"]
    work.mkdir(parents=True, exist_ok=True)

    assets = json.loads(run(["node", "engine/assets.mjs", args.episode], capture_output=True, text=True).stdout)
    voice = {
        "intro": tts(ep["intro"]["say"], 1.1),
        "levels": [tts(lv["say"], 1.0) for lv in ep["levels"]],
        "outro": tts(ep["outro"]["say"], 1.08),
    }
    tl = make_timeline(ep, assets, {"intro": len(voice["intro"]) / SR, "outro": len(voice["outro"]) / SR})
    tl_path = work / "timeline.json"
    tl_path.write_text(json.dumps(tl, ensure_ascii=False), encoding="utf-8")
    print(f"Durée : {tl['duration']:.1f} s  (accroche {tl['intro']['end']:.1f} s, {len(tl['levels'])} niveaux)")

    if args.stills:
        run(["node", "engine/render.mjs", tl_path, "--stills", work / "stills", args.stills])
        print(f"Images de contrôle : {work / 'stills'}")
        return

    audio, loud = soundtrack(tl, voice)
    sf.write(work / "audio.wav", audio, SR, subtype="PCM_16")
    print(f"Bande-son : {loud:.1f} LUFS avant normalisation, ramenée à -14")

    if not (args.audio_only and (work / "video.mp4").exists()):
        run(["node", "engine/render.mjs", tl_path, work / "video.mp4"])
    final = OUT / f"{ep['id']}.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", work / "video.mp4", "-i", work / "audio.wav", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", final])
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "2.4", "-i", final, "-frames:v", "1", "-q:v", "2", OUT / f"{ep['id']}-couverture.jpg"])
    post = ep.get("post", {})
    (OUT / f"{ep['id']}-legende.txt").write_text(
        post.get("caption", "") + "\n\n" + " ".join("#" + h for h in post.get("hashtags", [])) + "\n", encoding="utf-8")
    print(f"Vidéo prête : {final}")


if __name__ == "__main__":
    sys.exit(main())
