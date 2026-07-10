"""AeroForge PPT charts — palette validated (orange #eb6834 / blue #2a78d6)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import os

OUT = os.path.dirname(os.path.abspath(__file__)) + "/charts"
os.makedirs(OUT, exist_ok=True)

SURF = "#fcfcfb"; INK = "#0b0b0b"; SEC = "#52514e"; MUT = "#898781"
GRID = "#e1e0d9"; BASE = "#c3c2b7"
ORANGE = "#eb6834"; BLUE = "#2a78d6"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "text.color": INK,
    "axes.edgecolor": BASE, "axes.labelcolor": SEC,
    "xtick.color": MUT, "ytick.color": MUT,
    "figure.facecolor": SURF, "axes.facecolor": SURF,
    "svg.fonttype": "none",
})

def style_ax(ax, ygrid=True):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BASE)
    if ygrid:
        ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
    ax.tick_params(length=0)

# ---------------------------------------------------------------- chart 1
# Total Performance per quarter — AeroForge (class avg as annotations)
q = ["Q2", "Q3", "Q4", "Q5", "Q6"]
us = [0.013, 0.094, 0.266, 0.957, 3.494]
avg_txt = ["class avg 0.23", "0.94", "4.19", "n/a", "83.7"]

fig, ax = plt.subplots(figsize=(6.0, 4.1), dpi=200)
x = range(len(q))
ax.bar(x, us, width=0.5, color=ORANGE, zorder=3, edgecolor=SURF, linewidth=1.2)
for i, v in enumerate(us):
    ax.annotate(f"{v:.3f}", (i, v), textcoords="offset points", xytext=(0, 4),
                ha="center", fontsize=9.5, fontweight="bold", color=INK)
for i, t in enumerate(avg_txt):
    ax.annotate(t, (i, 0), textcoords="offset points", xytext=(0, -30),
                ha="center", fontsize=8, color=MUT, annotation_clip=False)
ax.annotate("×269 in 4 quarters", xy=(0.55, 2.9), fontsize=11, fontweight="bold", color=ORANGE)
ax.set_xticks(list(x)); ax.set_xticklabels(q, fontsize=10)
ax.set_ylim(0, 4.0)
ax.set_title("AeroForge Total Performance per quarter", fontsize=12.5, fontweight="bold",
             color=INK, loc="left", pad=14)
style_ax(ax)
fig.tight_layout()
fig.subplots_adjust(bottom=0.17)
fig.savefig(f"{OUT}/chart_totalperf.png", facecolor=SURF)
plt.close(fig)

# ---------------------------------------------------------------- chart 2
# Revenue & operating cash flow, one $k axis
q2 = ["Q2", "Q3", "Q4", "Q5", "Q6"]
rev = [226, 373, 740, 1440, 3018]
ocf = [-131, -86, -829, -1226, 748]

fig, ax = plt.subplots(figsize=(6.0, 4.1), dpi=200)
x = range(len(q2)); w = 0.36
ax.bar([i - w/2 for i in x], rev, width=w, color=ORANGE, zorder=3,
       edgecolor=SURF, linewidth=1.2, label="Revenue")
ax.bar([i + w/2 for i in x], ocf, width=w, color=BLUE, zorder=3,
       edgecolor=SURF, linewidth=1.2, label="Operating cash flow")
ax.axhline(0, color=BASE, linewidth=1.0, zorder=2)
for i, v in enumerate(rev):
    ax.annotate(f"{v:,}", (i - w/2, v), textcoords="offset points", xytext=(0, 4),
                ha="center", fontsize=8.5, fontweight="bold", color=INK)
for i, v in enumerate(ocf):
    off = 4 if v >= 0 else -12
    ax.annotate(f"{v:+,}", (i + w/2, v), textcoords="offset points", xytext=(0, off),
                ha="center", fontsize=8.5, color=SEC)
ax.annotate("$2.5M VC deployed:\nR&D, capacity, stores", xy=(1.0, -1450),
            fontsize=9, color=SEC, ha="center", style="italic")
ax.annotate("1st profitable\nquarter", xy=(4.18, 1050), fontsize=9.5,
            fontweight="bold", color="#006300", ha="center")
ax.set_xticks(list(x)); ax.set_xticklabels(q2, fontsize=10)
ax.set_ylim(-1650, 3500)
ax.set_title("Revenue & operating cash flow  ($ thousands)", fontsize=12.5,
             fontweight="bold", color=INK, loc="left", pad=14)
ax.legend(frameon=False, fontsize=9, loc="upper left", handlelength=1.2)
style_ax(ax)
fig.tight_layout()
fig.savefig(f"{OUT}/chart_finance.png", facecolor=SURF)
plt.close(fig)

# ---------------------------------------------------------------- chart 3
# Diagnose → fix → measure (dumbbell, all 0-100 scales)
rows = [
    ("Bolt ad judgment",        35.0, 80.0, "best Speed ad (Q4)"),
    ("Bolt brand judgment",     53.0, 87.0, "(Q6)"),
    ("Summit brand judgment",   62.0, 83.0, "top-2 Mountain (Q6)"),
    ("Comfy brand judgment",    65.0, 78.0, "top-2 Recreation (Q6)"),
    ("Worker productivity %",   68.6, 82.4, ""),
    ("Worker satisfaction %",   71.9, 88.0, ""),
]
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=200)
ys = list(range(len(rows)))[::-1]
for y, (label, a, b, note) in zip(ys, rows):
    ax.plot([a, b], [y, y], color=GRID, linewidth=2.4, zorder=2)
    ax.scatter([a], [y], s=90, color=BLUE, zorder=3, edgecolors=SURF, linewidths=1.4)
    ax.scatter([b], [y], s=90, color=ORANGE, zorder=3, edgecolors=SURF, linewidths=1.4)
    ax.annotate(f"{a:g}", (a, y), textcoords="offset points", xytext=(0, 10),
                ha="center", fontsize=9, color=SEC)
    txt = f"{b:g}"
    ax.annotate(txt, (b, y), textcoords="offset points", xytext=(0, 10),
                ha="center", fontsize=9, fontweight="bold", color=INK)
    if note:
        ax.annotate(note, (b, y), textcoords="offset points", xytext=(12, -3.5),
                    fontsize=8.5, color=ORANGE, fontweight="bold", va="center")
ax.set_yticks(ys)
ax.set_yticklabels([r[0] for r in rows], fontsize=10, color=INK)
ax.set_xlim(25, 118)
ax.set_xticks([40, 60, 80, 100])
ax.set_title("Diagnose → fix → measure", fontsize=12.5, fontweight="bold",
             color=INK, loc="left", pad=16)
# legend
ax.scatter([], [], s=90, color=BLUE, label="Before fix")
ax.scatter([], [], s=90, color=ORANGE, label="After fix")
ax.legend(frameon=False, fontsize=9, loc="lower left", scatterpoints=1)
style_ax(ax, ygrid=False)
ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
fig.tight_layout()
fig.savefig(f"{OUT}/chart_fixes.png", facecolor=SURF)
plt.close(fig)

print("charts written to", OUT)
