"""Figures 1, 3 and 4. Numbers are computed from the released files:
study1b/results/scored_items.csv and study2_prefix_repair/data/annotator_A.csv.
Usage: python make_figures_extra.py SCORED_ITEMS_CSV STUDY2_ANNOTATOR_A_CSV
"""
import collections
import csv
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch

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
BLUE, ORANGE, GRAY, INK, LIGHT = "#3f51b5", "#e2703a", "#a3a19b", "#33322f", "#e6e5e1"
TEAL = "#2e9e8f"


def style(ax, grid="y"):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if grid:
        getattr(ax, grid + "axis").grid(True, color=LIGHT, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, pad=3)


# ---------------- data ----------------
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
D = collections.defaultdict(dict)
for r in rows:
    D[r["model"]][r["item_id"]] = r
known = {m: {r["fact_id"] for r in d.values() if r["condition"] == "baseline" and r["label"] == "correct"}
         for m, d in D.items()}


def longc(m):
    return [r for r in D[m].values() if r["condition"] == "conflict" and r["length"] == "long"]


PAIRS = [("EleutherAI/pythia-160m", "state-spaces/mamba-130m-hf", "160M/130M"),
         ("EleutherAI/pythia-410m", "state-spaces/mamba-370m-hf", "410M/370M"),
         ("EleutherAI/pythia-1b", "state-spaces/mamba-790m-hf", "1B/790M"),
         ("EleutherAI/pythia-1.4b", "state-spaces/mamba-1.4b-hf", "1.4B/1.4B"),
         ("EleutherAI/pythia-2.8b", "state-spaces/mamba-2.8b-hf", "2.8B/2.8B")]
REFS = ["Qwen/Qwen2.5-0.5B", "Qwen/Qwen2.5-1.5B", "Qwen/Qwen2.5-3B", "HuggingFaceTB/SmolLM2-1.7B"]
SHORT = {"EleutherAI/pythia-160m": "Pythia-160M", "state-spaces/mamba-130m-hf": "Mamba-130M",
         "EleutherAI/pythia-410m": "Pythia-410M", "state-spaces/mamba-370m-hf": "Mamba-370M",
         "EleutherAI/pythia-1b": "Pythia-1B", "state-spaces/mamba-790m-hf": "Mamba-790M",
         "EleutherAI/pythia-1.4b": "Pythia-1.4B", "state-spaces/mamba-1.4b-hf": "Mamba-1.4B",
         "EleutherAI/pythia-2.8b": "Pythia-2.8B", "state-spaces/mamba-2.8b-hf": "Mamba-2.8B",
         "Qwen/Qwen2.5-0.5B": "Qwen2.5-0.5B", "Qwen/Qwen2.5-1.5B": "Qwen2.5-1.5B",
         "Qwen/Qwen2.5-3B": "Qwen2.5-3B", "HuggingFaceTB/SmolLM2-1.7B": "SmolLM2-1.7B"}
LOG = []

# ================= Figure 1: design =================
fig, ax = plt.subplots(figsize=(6.9, 2.9))
ax.set_xlim(0, 100)
ax.set_ylim(0, 40)
ax.axis("off")


def box(x, y, w, h, text, fc="white", ec="#9a9893", fs=7.3, bold=False, color=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.25,rounding_size=0.8",
                                fc=fc, ec=ec, lw=0.7))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color,
            fontweight="bold" if bold else "normal", linespacing=1.25)


def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#6b6a66", lw=0.7, mutation_scale=7))


ax.text(0.5, 38.5, "Study 1: swap the mixer, hold data fixed", fontsize=9, color=INK, fontweight="bold", va="top")
box(0.5, 20.5, 12.5, 13, "Same corpus\n(the Pile),\nsame tokenizer,\n5 matched sizes", fc="#f4f3ef", fs=6.8)
box(16, 28, 12.5, 5.5, "Pythia\n(attention)", fc="#e8ebf7", ec=BLUE, color=BLUE, bold=True)
box(16, 20.5, 12.5, 5.5, "Mamba\n(state space)", fc="#fcebe2", ec=ORANGE, color=ORANGE, bold=True)
arrow(13.3, 27, 15.8, 30.7)
arrow(13.3, 27, 15.8, 23.2)
box(31.5, 28.5, 17.5, 5, "No context:\nprior answer", fs=6.6)
box(31.5, 22.5, 17.5, 5, "False fact planted:\n3 positions x 2 lengths", fc="#fdf3ee", fs=6.6)
box(31.5, 16.5, 17.5, 5, "True fact planted:\nreading control", fc="#eef6f4", fs=6.6)
for yy in (31, 25, 19):
    arrow(28.8, 27, 31.3, yy)
ax.text(40.2, 13.6, "111 facts × 9 = 999 items per model", ha="center", fontsize=6.8, color="#6b6a66", style="italic")
box(1, 1.5, 47.5, 9.3, "Each conflict answer: repeats the planted fact,\nkeeps its own answer, or other.\nPaired McNemar test per matched pair.",
    fc="#f9f9f7", fs=6.5)

ax.plot([52, 52], [2, 38], color=LIGHT, lw=1)

ax.text(55, 38.5, "Study 2: replace the first wrong fact", fontsize=9, color=INK, fontweight="bold", va="top")
box(55, 27.5, 44, 6.5, "Q: Who developed Japan's first arc lamp?\n"
    "A: [wrong name], then employer, city, date ...", fc="#f4f3ef", fs=6.6)
ax.text(77, 25.6, "first divergence", ha="center", fontsize=6.6, color="#6b6a66", style="italic")
xs = [55, 66.3, 77.6, 88.9]
labels = [("A", "original\nanswer", "#f4f3ef", GRAY),
          ("B", "correct fact\ninserted", "#e8ebf7", BLUE),
          ("D", "other wrong\nfact inserted", "#fcebe2", ORANGE),
          ("C", "asked again,\nno prefix", "#eef6f4", TEAL)]
for x, (t, s, fc, ec) in zip(xs, labels):
    box(x, 14.5, 10.1, 8.5, "", fc=fc, ec=ec)
    ax.text(x + 5.05, 21, t, ha="center", va="center", fontsize=8.5, color=ec if ec != GRAY else INK, fontweight="bold")
    ax.text(x + 5.05, 17.3, s, ha="center", va="center", fontsize=6.3, color=INK, linespacing=1.15)
    arrow(77, 24.9, x + 5.05, 23.4)
box(55, 2, 44, 9.6, "111 committed errors from 3 models.\nTwo blind annotators count failing claims.\nH1: B < A     H2: C correct     H3: B < D", fc="#f9f9f7", fs=6.5)
fig.savefig("figures/fig_design.pdf", bbox_inches="tight", pad_inches=0.02)
fig.savefig("figures/fig_design.png", dpi=200, bbox_inches="tight", pad_inches=0.02)
plt.close(fig)

# ================= Figure 3: Study 1 in detail =================
fig, axs = plt.subplots(2, 2, figsize=(6.7, 4.9), gridspec_kw={"height_ratios": [1.05, 1], "width_ratios": [1.25, 1]})
(a, b), (c, d) = axs

# (a) composition of responses, 31-line conflict items
order = []
for p, m, _ in PAIRS:
    order += [p, m]
order += REFS
ypos, yy = [], 0
for i, m in enumerate(order):
    ypos.append(yy)
    yy += 1 if (i % 2 == 0 and i < 10) else 1.55
ypos = [max(ypos) - v for v in ypos]
for m, y in zip(order, ypos):
    L = longc(m)
    n = len(L)
    f = sum(r["label"] == "followed" for r in L) / n * 100
    pr = sum(r["label"] == "prior" for r in L) / n * 100
    ot = 100 - f - pr
    LOG.append(f"composition {SHORT[m]}: followed {f:.1f} prior {pr:.1f} other {ot:.1f}")
    col = ORANGE if "mamba" in m else BLUE
    a.barh(y, f, 0.82, color=col, zorder=3)
    a.barh(y, pr, 0.82, left=f, color=TEAL, zorder=3)
    a.barh(y, ot, 0.82, left=f + pr, color="#d9d7d1", zorder=3)
a.set_yticks(ypos, [SHORT[m] for m in order], fontsize=6.8)
a.set_xlim(0, 100)
a.set_xticks([0, 25, 50, 75, 100])
style(a, "x")
a.set_title("(a) What happens to a planted falsehood", loc="left", color=INK)
a.set_xlabel("% of 31-line conflict items")
from matplotlib.patches import Patch
a.legend(handles=[Patch(color=BLUE, label="repeats it (attention)"), Patch(color=ORANGE, label="repeats it (state space)"),
                  Patch(color=TEAL, label="keeps own answer"), Patch(color="#d9d7d1", label="other")],
         frameon=False, fontsize=6.5, loc="upper center", bbox_to_anchor=(0.45, -0.17), ncol=2, handlelength=1, columnspacing=1)

# (b) prior knowledge vs following rate
for m in order:
    L = longc(m)
    f = sum(r["label"] == "followed" for r in L) / len(L) * 100
    k = len(known[m])
    ssm = "mamba" in m
    ref = m in REFS
    b.scatter(k, f, s=26 if not ref else 22, marker="s" if ssm else ("D" if ref else "o"),
              color=ORANGE if ssm else BLUE, alpha=1 if not ref else 0.55, zorder=3, edgecolor="white", linewidth=0.5)
    lab = SHORT[m].replace("Pythia-", "P-").replace("Mamba-", "M-")
    if not ref:
        off = {"M-1.4B": (-4, -7), "M-2.8B": (-14, 2), "M-790M": (-13, -8), "M-370M": (3, -2), "M-130M": (3, 3),
               "P-160M": (3, -8), "P-410M": (2, -8), "P-1B": (2, 3), "P-1.4B": (-26, -3), "P-2.8B": (3, -10)}[lab]
        b.annotate(lab, (k, f), xytext=off, textcoords="offset points", fontsize=6.2, color=INK)
b.text(108, 104, "Qwen, SmolLM2", fontsize=6.2, color="#7b7a76", ha="right")
b.set_xlim(-3, 116)
b.set_ylim(20, 107)
b.set_xlabel("facts known without context (of 111)")
b.set_ylabel("% repeating the planted fact")
style(b, None)
b.yaxis.grid(True, color=LIGHT, linewidth=0.6)
b.xaxis.grid(True, color=LIGHT, linewidth=0.6)
b.set_title("(b) Prior knowledge and deference", loc="left", color=INK)

# (c) facts both models knew: dumbbell per pair
for i, (p, m, lab) in enumerate(PAIRS[1:]):
    kn = known[p] & known[m]
    Lp = [r for r in longc(p) if r["fact_id"] in kn]
    Lm = [r for r in longc(m) if r["fact_id"] in kn]
    fp = sum(r["label"] == "followed" for r in Lp) / len(Lp) * 100
    fm_ = sum(r["label"] == "followed" for r in Lm) / len(Lm) * 100
    LOG.append(f"known-both {lab}: n={len(Lp)} pythia {fp:.1f} mamba {fm_:.1f}")
    y = 3 - i
    c.plot([fm_, fp], [y, y], color="#c9c7c1", lw=2.2, zorder=2, solid_capstyle="round")
    c.scatter([fp], [y], color=BLUE, s=34, zorder=3)
    c.scatter([fm_], [y], color=ORANGE, s=34, marker="s", zorder=3)
    c.text(fp + 2.5, y, f"{fp:.0f}", va="center", fontsize=6.6, color=BLUE)
    c.text(fm_ - 2.5, y, f"{fm_:.0f}", va="center", ha="right", fontsize=6.6, color=ORANGE)
c.set_yticks([3, 2, 1, 0], [f"{x[2]}\nn = {len(known[x[0]] & known[x[1]]) * 3}" for x in PAIRS[1:]], fontsize=6.8)
c.set_xlim(0, 108)
c.set_ylim(-0.6, 3.6)
c.set_xticks([0, 25, 50, 75, 100])
c.set_xlabel("% repeating the planted fact (facts both knew)")
style(c, "x")
c.set_title("(c) Facts both models knew, 31-line text", loc="left", color=INK)

# (d) position, pooled over the four interpretable pairs
pos = ["early", "middle", "late"]
for grp, col, mk, lab in ((0, BLUE, "o", "Pythia (4 models)"), (1, ORANGE, "s", "Mamba (4 models)")):
    ms = [x[grp] for x in PAIRS[1:]]
    vals = []
    for pp in pos:
        sel = [r for m in ms for r in longc(m) if r["position"] == pp]
        vals.append(sum(r["label"] == "followed" for r in sel) / len(sel) * 100)
    LOG.append(f"position {lab}: " + " ".join(f"{v:.1f}" for v in vals) + f" (n={len(sel)} per position)")
    d.plot(range(3), vals, color=col, lw=1.8, marker=mk, ms=4.5, zorder=3, label=lab)
    for i, v in enumerate(vals):
        d.text(i, v + (2.6 if grp == 0 else -6.5), f"{v:.0f}", ha="center", fontsize=6.6, color=col)
d.set_xticks(range(3), ["first", "middle", "last"])
d.set_xlim(-0.35, 2.35)
d.set_ylim(30, 105)
d.set_xlabel("position of the planted line in a 31-line text")
style(d)
d.legend(frameon=False, fontsize=6.6, loc="lower left")
d.set_title("(d) Position of the planted line", loc="left", color=INK)

fig.tight_layout(h_pad=1.6, w_pad=1.4)
fig.savefig("figures/fig_study1_detail.pdf")
fig.savefig("figures/fig_study1_detail.png", dpi=200)
plt.close(fig)

# ================= Figure 4: Study 2 in detail =================
rows2 = list(csv.DictReader(open(sys.argv[2], encoding="utf-8")))
it = collections.defaultdict(dict)
for r in rows2:
    it[(r["item_id"], r["model"])][r["condition"]] = r


def refused(r):
    return r["abstain"].strip() in ("1", "1.0")


def nfail(r):
    return float(r["n_downstream_failing"])


S = [(k, v) for k, v in it.items() if not refused(v["b_substituted"]) and not refused(v["d_control"])]
fig, (a, b) = plt.subplots(1, 2, figsize=(6.7, 2.6), gridspec_kw={"width_ratios": [1.15, 1]})
conds = [("a_baseline", "Original"), ("b_substituted", "Correct fact"), ("d_control", "Wrong fact")]
shades = ["#eef6f4", "#c6dcd8", "#94bfb8", "#5f9e95", "#2f6f66"]
for i, (cc, lab) in enumerate(conds):
    cnt = collections.Counter(min(int(nfail(v[cc])), 4) for _, v in S)
    left = 0
    LOG.append(f"claims {lab}: " + str(dict(sorted(cnt.items()))))
    for kk in range(5):
        w = cnt.get(kk, 0)
        a.barh(2 - i, w, 0.62, left=left, color=shades[kk], zorder=3, edgecolor="white", linewidth=0.6)
        if w >= 6:
            a.text(left + w / 2, 2 - i, str(w), ha="center", va="center", fontsize=6.6,
                   color="white" if kk >= 3 else INK)
        left += w
a.set_yticks([2, 1, 0], [x[1] for x in conds])
a.set_xlim(0, 97)
a.set_xlabel("items (n = 97), shaded by number of failing claims")
style(a, "x")
a.set_title("(a) Failing claims after the divergence", loc="left", color=INK)
a.legend(handles=[Patch(color=shades[k], label=lab) for k, lab in enumerate(["0", "1", "2", "3", "4+"])],
         frameon=False, fontsize=6.5, ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.52), handlelength=1, columnspacing=1)

models = [("allam-2-7b", "ALLaM-2-7B"), ("openai/gpt-oss-120b", "GPT-OSS-120B"), ("qwen/qwen3.6-27b", "Qwen3.6-27B")]
w = 0.26
NS = []
for j, (mid, ml) in enumerate(models):
    ss = [v for k, v in S if k[1] == mid]
    vals = [sum(nfail(v[cc]) > 0 for v in ss) / len(ss) * 100 for cc, _ in conds]
    LOG.append(f"per-model {ml}: n={len(ss)} " + " ".join(f"{v:.1f}" for v in vals))
    for i, (v, col) in enumerate(zip(vals, [GRAY, BLUE, ORANGE])):
        b.bar(j + (i - 1) * w, v, w, color=col, zorder=3, label=conds[i][1] if j == 0 else None)
    NS.append(f"{ml}\nn = {len(ss)}")
b.set_xticks(range(3), NS, fontsize=7)
b.set_ylim(0, 122)
b.set_yticks([0, 25, 50, 75, 100])
b.set_ylabel("% with an error")
style(b)
b.legend(frameon=False, fontsize=6.5, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.2), handlelength=1, columnspacing=1)
b.set_title("(b) By model", loc="left", color=INK, pad=20)
fig.tight_layout(w_pad=2)
fig.savefig("figures/fig_study2_detail.pdf", bbox_inches="tight", pad_inches=0.03)
fig.savefig("figures/fig_study2_detail.png", dpi=200, bbox_inches="tight", pad_inches=0.03)
open("figures/figure_values.txt", "w").write("\n".join(LOG) + "\n")
print("\n".join(LOG))
