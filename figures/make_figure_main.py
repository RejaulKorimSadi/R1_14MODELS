"""Figure 1. All values are taken from the released analysis outputs (see supplementary README)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

FD = "/usr/share/fonts/opentype/linux-libertine/"
HAVE_FONT = True
for f in ("LinBiolinum_R.otf", "LinBiolinum_RB.otf", "LinBiolinum_RI.otf"):
    try:
        fm.fontManager.addfont(FD + f)
    except (FileNotFoundError, OSError):
        HAVE_FONT = False
plt.rcParams.update({"font.family": "Linux Biolinum O" if HAVE_FONT else "sans-serif", 
    "font.size": 8.5, "pdf.fonttype": 42,
    "axes.edgecolor": "#9a9893", "axes.linewidth": 0.6, "axes.labelcolor": "#33322f",
    "xtick.color": "#4a4945", "ytick.color": "#4a4945", "axes.titlesize": 9,
})
BLUE, ORANGE, GRAY, INK = "#3f51b5", "#e2703a", "#a3a19b", "#33322f"


def style(ax, ymax=105):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_ylim(0, ymax)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.yaxis.grid(True, color="#e6e5e1", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, pad=3)


fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(6.7, 2.55), gridspec_kw={"width_ratios": [1.25, 1.15, 0.8]})

# (a) follow rate by matched pair
x = list(range(5))
labs = ["160M\n130M", "410M\n370M", "1B\n790M", "1.4B\n1.4B", "2.8B\n2.8B"]
PS = [55.3, 99.4, 98.8, 98.2, 99.7]
PL = [38.4, 94.6, 97.3, 96.4, 95.5]
MS = [44.4, 77.5, 91.9, 26.4, 93.7]
ML = [36.9, 50.8, 70.9, 29.4, 76.3]
a1.axvspan(-0.45, 0.45, color="#f2f1ed", zorder=0)
a1.text(0, 101, "weak\nreading", ha="center", va="top", fontsize=6.5, color="#8a8984", style="italic")
a1.plot(x, PS, ls=(0, (3, 2)), color=BLUE, lw=1, marker="o", ms=2.8, mfc="white", zorder=3)
a1.plot(x, PL, color=BLUE, lw=1.8, marker="o", ms=3.8, zorder=4)
a1.plot(x, MS, ls=(0, (3, 2)), color=ORANGE, lw=1, marker="s", ms=2.8, mfc="white", zorder=3)
a1.plot(x, ML, color=ORANGE, lw=1.8, marker="s", ms=3.8, zorder=4)
a1.text(4.15, PL[-1] - 1, "Pythia", color=BLUE, fontsize=8, va="center", fontweight="bold")
a1.text(4.15, ML[-1], "Mamba", color=ORANGE, fontsize=8, va="center", fontweight="bold")
a1.set_xlim(-0.5, 4.95)
a1.set_xticks(x, labs, fontsize=7.2)
a1.set_ylabel("% repeating the planted false fact")
style(a1)
a1.set_title("(a) By matched pair", loc="left", color=INK)
a1.plot([], [], color="#555", lw=1.8, label="31-line text")
a1.plot([], [], color="#555", lw=1, ls=(0, (3, 2)), label="9-line text")
a1.legend(frameon=False, fontsize=7, loc="lower right", bbox_to_anchor=(0.86, 0.0), handlelength=2.2)

# (b) by fact type, pooled 410M-2.8B pairs, 31-line
names = ["Author", "Symbol", "Currency", "Painter", "Capital", "Planet"]
P = [83, 97, 96, 97, 99, 97]
M = [35, 37, 53, 62, 67, 67]
w = 0.38
a2.bar([i - w / 2 for i in range(6)], P, w, color=BLUE, zorder=3, label="Pythia")
a2.bar([i + w / 2 for i in range(6)], M, w, color=ORANGE, zorder=3, label="Mamba")
for i, v in enumerate(M):
    a2.text(i + w / 2, v + 1.5, f"{v}", ha="center", fontsize=6.3, color=INK)
a2.set_xticks(range(6), names, fontsize=7.2, rotation=35, ha="right", rotation_mode="anchor")
style(a2, 112)
a2.set_title("(b) By fact type, 31-line text", loc="left", color=INK)
a2.legend(frameon=False, fontsize=7, loc="upper right", ncol=2, bbox_to_anchor=(1.02, 1.04), handlelength=1, columnspacing=0.8)

# (c) Study 2 on 97 jointly scored items: 92, 44, 38 with a downstream error
vals = [92 / 97 * 100, 44 / 97 * 100, 38 / 97 * 100]
for i, (v, c) in enumerate(zip(vals, [GRAY, BLUE, ORANGE])):
    a3.bar(i, v, 0.62, color=c, zorder=3)
    a3.text(i, v + 2 if i != 1 else v - 7, f"{v:.0f}%", ha="center", fontsize=7.2, color="white" if i == 1 else INK)
a3.plot([1, 1, 2, 2], [53, 60, 60, 46], color="#6b6a66", lw=0.7)
a3.text(1.5, 62.5, "p = 0.38", ha="center", fontsize=6.8, color="#4a4945")
a3.set_xticks(range(3), ["Original", "Correct\nfact", "Wrong\nfact"], fontsize=7.2)
a3.set_ylabel("% with a downstream error")
style(a3)
a3.set_title("(c) First error replaced", loc="left", color=INK)

fig.tight_layout(w_pad=1.6)
fig.savefig("figures/fig_results.pdf")
fig.savefig("figures/fig_results.png", dpi=200)
