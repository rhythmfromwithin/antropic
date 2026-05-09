import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
import numpy as np

# ── Claude Brand Colors ────────────────────────────────────────────────────
BG       = "#faf9f5"   # cream canvas
BG_MID   = "#eeece2"   # section fill
BORDER   = "#e8e6dc"
TEXT     = "#3d3929"   # warm dark brown
MUTED    = "#7c7a6e"
SUBTLE   = "#b0aea5"
ORANGE   = "#d97757"   # terra cotta
ORANGE_D = "#bd5d3a"
BLUE     = "#6a9bcc"
GREEN    = "#788c5d"

# competitor colors
C_OPENAI = "#10A37F"
C_GOOGLE = "#4285F4"
C_MSFT   = "#0078D4"
C_AWS    = "#FF9900"
C_COHERE = "#8B5CF6"
C_META   = "#1877F2"

OUT = "/Users/gztd-03-02619/Q2/the_future/"

plt.rcParams.update({
    "font.family":       "sans-serif",
    "font.size":         12,
    "axes.titlesize":    14,
    "axes.titleweight":  "bold",
    "axes.titlepad":     16,
    "axes.labelsize":    11,
    "axes.labelcolor":   MUTED,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.spines.left":  True,
    "axes.spines.bottom":True,
    "axes.edgecolor":    BORDER,
    "xtick.color":       MUTED,
    "ytick.color":       MUTED,
    "xtick.labelsize":   10,
    "ytick.labelsize":   10,
    "figure.facecolor":  BG,
    "axes.facecolor":    BG,
    "grid.color":        BORDER,
    "grid.linewidth":    0.8,
})

def save(name):
    plt.savefig(OUT + name, dpi=160, bbox_inches="tight",
                facecolor=BG, edgecolor="none")
    plt.close()
    print(f"  {name}")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 1 — ARR Comparison
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 4.5))
fig.subplots_adjust(left=0.32, right=0.88, top=0.82, bottom=0.14)

companies = ["Anthropic (gross)", "OpenAI", "Anthropic (disputed net)"]
arr       = [30, 25, 22]
clrs      = [ORANGE, C_OPENAI, ORANGE]
alphas    = [1.0, 1.0, 0.38]

for i, (comp, val, clr, al) in enumerate(zip(companies, arr, clrs, alphas)):
    ax.barh(i, val, color=clr, alpha=al, height=0.52, zorder=2)
    ax.text(val + 0.6, i, f"${val}B", va="center", ha="left",
            fontsize=13, fontweight="bold", color=TEXT)

ax.set_yticks(range(len(companies)))
ax.set_yticklabels(companies, fontsize=11)
ax.set_xlim(0, 38)
ax.set_xlabel("ARR  ($B,  April 2026)", labelpad=8)
ax.set_title("ARR Comparison: Anthropic vs OpenAI", color=TEXT)
ax.axvline(22, color=ORANGE, ls="--", alpha=0.45, lw=1.4)

note = mpatches.Patch(color=ORANGE, alpha=0.38,
                      label="~$8B dispute: gross vs. net revenue recognition on AWS/GCP deals")
ax.legend(handles=[note], fontsize=9, loc="lower right",
          framealpha=0, labelcolor=MUTED)
ax.yaxis.set_tick_params(length=0)
ax.set_facecolor(BG)
save("chart1_arr_comparison.png")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 2 — Developer Community Scale
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 5))
fig.subplots_adjust(left=0.1, right=0.95, top=0.82, bottom=0.22)

labels = ["OpenAI", "Google\nGemini", "AWS\nBedrock", "Cohere\n(enterprise)"]
devs   = [4_000_000, 2_400_000, 100_000, 17_000]
clrs   = [C_OPENAI, C_GOOGLE, C_AWS, C_COHERE]

bars = ax.bar(labels, devs, color=clrs, width=0.52, zorder=2)
ax.set_ylabel("Active Developers / Organizations")
ax.set_title("API Developer Community Scale  (May 2026)", color=TEXT)
ax.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, _: f"{x/1e6:.1f}M" if x >= 1e6 else f"{int(x/1000)}K"))
ax.set_ylim(0, 4_800_000)
ax.yaxis.grid(True, zorder=0)
ax.set_axisbelow(True)

for bar, val in zip(bars, devs):
    label = f"{val/1e6:.1f}M" if val >= 1e6 else f"{val:,}"
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 60_000,
            label, ha="center", va="bottom", fontsize=12, fontweight="bold", color=TEXT)

ax.text(0.5, -0.18,
        "Anthropic developer community not publicly disclosed.\n"
        "70× API volume YoY signals intensity per developer — not breadth vs. competitors.",
        ha="center", transform=ax.transAxes, fontsize=9, color=MUTED, linespacing=1.6)
save("chart2_developer_scale.png")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 3 — RICE: Channels (left) + Experiments (right)
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(13, 6))
fig.subplots_adjust(left=0.07, right=0.97, top=0.80, bottom=0.22, wspace=0.35)

# 3a channels
ch_labels = ["Docs /\nRunnable\nSamples", "Claude Code\n→ API\nOn-ramp", "Bedrock\nIncrement-\nality", "Developer\nCommunity"]
ch_scores = [52_500, 16_250, 0, 625]
ch_notes  = ["Scale #1", "Scale #2", "Research", "Build 6–12mo"]
ch_clrs   = [GREEN, ORANGE, SUBTLE, BLUE]

ax = axes[0]
bars = ax.bar(ch_labels, ch_scores, color=ch_clrs, width=0.52, zorder=2)
ax.set_title("Acquisition Channels\nRICE Score", color=TEXT)
ax.set_ylabel("RICE Score")
ax.yaxis.grid(True, zorder=0); ax.set_axisbelow(True)
ax.set_ylim(0, 62_000)
for bar, score, note in zip(bars, ch_scores, ch_notes):
    if score > 500:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 800,
                f"{score:,}", ha="center", va="bottom", fontsize=11, fontweight="bold", color=TEXT)
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3_500,
                note, ha="center", va="bottom", fontsize=9, color=MUTED)
    else:
        ax.text(bar.get_x() + bar.get_width()/2, 1_200,
                note, ha="center", va="bottom", fontsize=9, color=MUTED)

# 3b experiments
exp_labels = ["E1: In-console\nQuickstart", "E2: Upgrade\nCTA at Limits", "E3: Claude Code\n→ API Path"]
exp_scores = [52_500, 14_625, 15_000]
exp_notes  = ["#1 · 2 weeks", "#2 · 2 weeks", "#3 · validate\nassumption first"]
exp_clrs   = [GREEN, ORANGE, BLUE]

ax = axes[1]
bars = ax.bar(exp_labels, exp_scores, color=exp_clrs, width=0.52, zorder=2)
ax.set_title("Days 31–60 Experiments\nRICE Score", color=TEXT)
ax.yaxis.grid(True, zorder=0); ax.set_axisbelow(True)
ax.set_ylim(0, 62_000)
for bar, score, note in zip(bars, exp_scores, exp_notes):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 800,
            f"{score:,}", ha="center", va="bottom", fontsize=11, fontweight="bold", color=TEXT)
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 4_000,
            note, ha="center", va="bottom", fontsize=9, color=MUTED)

fig.text(0.5, 0.04,
         "RICE = (Reach × Impact × Confidence) / Effort (person-weeks)  ·  E3 requires Week 1 assumption validation before any build decision",
         ha="center", fontsize=9, color=MUTED)
save("chart3_rice_scores.png")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 4 — OST POC Scores
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 5.5))
fig.subplots_adjust(left=0.1, right=0.95, top=0.80, bottom=0.28)

pocs        = ["A1: In-console\nInteractive Quickstart", "B1: Contextual\nUpgrade Modal", "C1: Claude Code\n→ API On-ramp"]
feasibility = [4, 4, 3]
impact      = [4, 5, 3]
market_fit  = [5, 5, 4]
totals      = [f+i+m for f, i, m in zip(feasibility, impact, market_fit)]

x = np.arange(len(pocs))
w = 0.24
ax.bar(x - w, feasibility, w, label="Feasibility", color=GREEN,   zorder=2)
ax.bar(x,     impact,      w, label="Impact",      color=ORANGE,  zorder=2)
ax.bar(x + w, market_fit,  w, label="Market Fit",  color=BLUE,    zorder=2)

ax.set_xticks(x)
ax.set_xticklabels(pocs, fontsize=10)
ax.set_ylim(0, 7.4)
ax.set_ylabel("Score  (1 – 5)")
ax.set_title("OST Recommended POCs — Feasibility · Impact · Market Fit", color=TEXT)
ax.yaxis.grid(True, zorder=0); ax.set_axisbelow(True)
ax.legend(fontsize=10, framealpha=0, loc="upper right")

for xi, total in zip(x, totals):
    ax.text(xi, 6.15, f"Total: {total}/15",
            ha="center", fontsize=11, fontweight="bold", color=TEXT,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=BG_MID, edgecolor=BORDER, lw=1))

fig.text(0.5, 0.06,
         "C1 requires assumption validation first: what % of Claude Code subscribers are already direct API users?\n"
         "If >80% already converted → redirect effort to expansion.  If <40% → build C1.",
         ha="center", fontsize=9, color=MUTED, linespacing=1.6)
save("chart4_ost_scores.png")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 5 — Competitor Positioning Matrix
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 6.5))
fig.subplots_adjust(left=0.13, right=0.95, top=0.88, bottom=0.14)

comp_data = {
    "Meta Llama\n(free / OSS)": (1.2, 3.0, C_META,   280, "right"),
    "Google Gemini":             (2.2, 4.2, C_GOOGLE, 320, "right"),
    "AWS Bedrock":               (4.0, 5.0, C_AWS,    280, "right"),
    "Microsoft\nAzure AI":       (5.2, 6.2, C_MSFT,   280, "right"),
    "OpenAI API":                (7.0, 5.2, C_OPENAI, 280, "left"),
    "Cohere":                    (6.2, 7.2, C_COHERE, 220, "right"),
    "Anthropic Claude":          (6.5, 9.2, ORANGE,   420, "left"),
}
for label, (px, py, clr, sz, side) in comp_data.items():
    ax.scatter(px, py, s=sz, color=clr, alpha=0.88, zorder=4,
               edgecolors="white", linewidths=2)
    ox = 0.22 if side == "right" else -0.22
    ha = "left" if side == "right" else "right"
    ax.text(px + ox, py, label, fontsize=9.5, va="center", ha=ha,
            color=TEXT, zorder=5,
            bbox=dict(boxstyle="round,pad=0.18", facecolor=BG, edgecolor="none", alpha=0.85))

ax.set_xlim(0, 11); ax.set_ylim(0, 11)
ax.set_xlabel("← Cheaper   ·   Relative Price Tier   ·   More Expensive →", labelpad=10)
ax.set_ylabel("← Marketing claim   ·   Safety Architecture   ·   Verifiable →", labelpad=10)
ax.set_title("Competitor Positioning: Price vs. Safety Architecture Depth", color=TEXT)

ax.axhline(7, ls="--", color=SUBTLE, lw=1.2, alpha=0.7)
ax.axvline(5, ls="--", color=SUBTLE, lw=1.2, alpha=0.7)
ax.text(0.3, 7.25, "Regulated-industry threshold", fontsize=9, color=SUBTLE)
ax.fill_between([5, 11], [7, 7], [11, 11], color=ORANGE, alpha=0.05, zorder=0)
ax.text(8.5, 10.3, "Target zone", fontsize=9, color=ORANGE_D, fontweight="bold")

ax.set_facecolor(BG)
save("chart5_competitor_matrix.png")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 6 — Business Health Scorecard (horizontal bars)
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 4.8))
fig.subplots_adjust(left=0.26, right=0.97, top=0.85, bottom=0.08)

dims    = ["Growth &\nRetention", "Unit\nEconomics", "Capital\nEfficiency", "Strategic\nPosition"]
scores  = [5, 3, 3, 4]          # out of 5
clrs    = [GREEN, ORANGE, ORANGE, GREEN]
labels  = [
    "EXCEPTIONAL — 70× API YoY; $1M+ accounts 12 → 500+",
    "MUST BASELINE — CAC/LTV not yet instrumented for self-serve",
    "WATCH — Revenue dispute adds noise; strong underlying trajectory",
    "STRONG (gaps) — MCP moat, Conway; developer community breadth lags",
]

y = np.arange(len(dims))
ax.barh(y, scores, color=clrs, height=0.52, alpha=0.85, zorder=2)
ax.set_yticks(y)
ax.set_yticklabels(dims, fontsize=11)
ax.set_xlim(0, 7.2)
ax.set_xlabel("Score  (out of 5)")
ax.set_title("Business Health Scorecard — Claude Platform API", color=TEXT)
ax.xaxis.grid(True, zorder=0); ax.set_axisbelow(True)
ax.yaxis.set_tick_params(length=0)

for i, (score, lbl) in enumerate(zip(scores, labels)):
    ax.text(score + 0.12, i, lbl, va="center", ha="left",
            fontsize=9, color=MUTED)

ax.text(0.5, -0.08,
        "Overall verdict: Strong Growth, Underbuilt Self-Serve.  Fix the funnel — the economics are already good.",
        ha="center", transform=ax.transAxes, fontsize=10, color=TEXT, fontweight="bold")
save("chart6_health_scorecard.png")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 7 — Risk Matrix
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9.5, 7))
fig.subplots_adjust(left=0.12, right=0.97, top=0.88, bottom=0.1)

risks = [
    ("Model releases\ninvalidate experiments",       3, 2, ORANGE),
    ("Eng capacity consumed\nby model infra",         3, 3, ORANGE_D),
    ("Meta Llama free tier\npulls cost-sensitive",    3, 3, ORANGE_D),
    ("Google $2/M pricing\npressure",                 2, 3, ORANGE),
    ("Revenue accounting\nmetric noise",              1, 2, BLUE),
    ("Claude Code→API\nassumption invalid",           2, 2, BLUE),
    ("Bedrock channel\nconflict",                     2, 2, BLUE),
    ("Enterprise expansion\nblocked by procurement",  2, 3, ORANGE),
]

# fixed offsets per point to avoid overlap
offsets = [(10, 10), (-90, 12), (10, -44), (10, 10), (10, 10), (-92, -40), (10, -44), (-105, 12)]

rng = np.random.default_rng(42)
for (label, lkh, imp, clr), (ox, oy) in zip(risks, offsets):
    jx = lkh + rng.uniform(-0.08, 0.08)
    jy = imp  + rng.uniform(-0.08, 0.08)
    ax.scatter(jx, jy, s=340, color=clr, alpha=0.80, zorder=4,
               edgecolors="white", linewidths=2)
    ax.annotate(label, (jx, jy), textcoords="offset points",
                xytext=(ox, oy), fontsize=9, color=TEXT, va="center",
                arrowprops=dict(arrowstyle="-", color=SUBTLE, lw=0.8),
                bbox=dict(boxstyle="round,pad=0.3", facecolor=BG, edgecolor=BORDER, lw=0.8))

ax.set_xlim(0.4, 3.7); ax.set_ylim(0.4, 3.7)
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(["Low", "Medium", "High"], fontsize=11)
ax.set_yticks([1, 2, 3]); ax.set_yticklabels(["Low", "Medium", "High"], fontsize=11)
ax.set_xlabel("Likelihood", labelpad=10)
ax.set_ylabel("Impact", labelpad=10)
ax.set_title("Risk Matrix — 30-60-90 Day Plan", color=TEXT)
ax.fill_between([2.5, 3.7], [2.5, 2.5], [3.7, 3.7], color="#fde8e8", alpha=0.5, zorder=0)
ax.text(3.05, 3.55, "Act now", fontsize=10, color="#b91c1c", fontweight="bold")
ax.grid(True, color=BORDER, zorder=0); ax.set_axisbelow(True)
save("chart7_risk_matrix.png")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 8 — KPI Framework (horizontal grouped)
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(11, 5.5))
fig.subplots_adjust(left=0.28, right=0.97, top=0.88, bottom=0.08)

metrics = [
    "$10K→$100K ARR\nexpansion",
    "Free → paid\nconversion",
    "D7 retention",
    "TTFAC <5 min\nrate",
    "Claude Code →\nAPI conversion",
    "New API\nsignups/week",
]
d30  = ["Baseline W1", "Baseline W1", "Measure", "Measure", "Instrument W1", "Baseline W1"]
d60  = ["Track rate",  "+20%",        ">40% PLG P75", "≥50% signups", "+30%", "Baseline +20%"]

y = np.arange(len(metrics))
h = 0.35
b1 = ax.barh(y + h/2, [1]*len(metrics), h, color=BG_MID,  edgecolor=BORDER, lw=1, zorder=2)
b2 = ax.barh(y - h/2, [1]*len(metrics), h, color=ORANGE,  alpha=0.25, edgecolor=ORANGE, lw=1, zorder=2)

ax.set_yticks(y)
ax.set_yticklabels(metrics, fontsize=10.5)
ax.set_xlim(0, 3.2)
ax.set_xticks([0.5, 1.5])
ax.set_xticklabels(["Days 1–30", "Days 31–60"], fontsize=11)
ax.set_title("KPI Framework — Targets by Phase", color=TEXT)
ax.yaxis.set_tick_params(length=0)

for i, (t30, t60) in enumerate(zip(d30, d60)):
    ax.text(0.5, i + h/2, t30, ha="center", va="center", fontsize=9.5, color=MUTED)
    ax.text(1.5, i - h/2, t60, ha="center", va="center", fontsize=9.5,
            color=ORANGE_D, fontweight="bold")

ax.text(0.5, -0.07,
        "D30 retention measurable only for cohorts from Days 1–60  ·  E3 requires Week 1 instrumentation as prerequisite",
        ha="center", transform=ax.transAxes, fontsize=9, color=MUTED)
save("chart8_kpi_framework.png")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 9 — Growth Signals (3 panels)
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(12, 5))
fig.subplots_adjust(left=0.07, right=0.97, top=0.80, bottom=0.18, wspace=0.4)
fig.suptitle("Anthropic Growth Signals  (May 2026)", fontsize=14,
             fontweight="bold", color=TEXT, y=0.96)

# 9a
ax = axes[0]
ax.bar(["Jan 2025", "Apr 2026"], [12, 500],
       color=[SUBTLE, ORANGE], width=0.45, zorder=2)
ax.set_title("$1M+ ARR Accounts", color=TEXT, fontsize=12)
ax.set_ylabel("Count")
ax.yaxis.grid(True, zorder=0); ax.set_axisbelow(True)
ax.set_ylim(0, 580)
ax.text(0, 28,  "12",    ha="center", fontsize=12, fontweight="bold", color="white")
ax.text(1, 516, "500+",  ha="center", fontsize=12, fontweight="bold", color=ORANGE)
ax.text(1, 548, "41×",   ha="center", fontsize=11, color=ORANGE_D, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#fdf5f0", edgecolor=ORANGE, lw=1))

# 9b
ax = axes[1]
months = ["Jan 2026", "May 2026"]
vals   = [100, 400]
ax.plot(months, vals, "o-", color=ORANGE, lw=2.8, ms=9, zorder=3)
ax.fill_between(months, vals, alpha=0.10, color=ORANGE, zorder=2)
ax.set_title("Claude Code Business\nSubscriptions  (Index 100 = Jan 2026)", color=TEXT, fontsize=11)
ax.set_ylabel("Index")
ax.set_ylim(0, 470)
ax.yaxis.grid(True, zorder=0); ax.set_axisbelow(True)
ax.text(0, 112, "100", ha="center", fontsize=11, color=MUTED)
ax.text(1, 412, "400", ha="center", fontsize=11, fontweight="bold", color=ORANGE)
ax.text(0.5, 440, "4×  growth", ha="center", fontsize=12,
        color=ORANGE_D, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#fdf5f0", edgecolor=ORANGE, lw=1))

# 9c
ax = axes[2]
platforms = ["Claude Code\n(Anthropic)", "Industry\nAverage*"]
hours     = [20, 5]
bars      = ax.bar(platforms, hours, color=[ORANGE, SUBTLE], width=0.42, zorder=2)
ax.set_title("Developer Engagement\n(Hours / Week)", color=TEXT, fontsize=12)
ax.set_ylabel("Avg hrs / week")
ax.set_ylim(0, 26)
ax.yaxis.grid(True, zorder=0); ax.set_axisbelow(True)
for bar, h in zip(bars, hours):
    ax.text(bar.get_x() + bar.get_width()/2, h + 0.5, f"{h}h",
            ha="center", va="bottom", fontsize=13, fontweight="bold", color=TEXT)
ax.text(0.5, -0.16, "* Industry average estimated",
        ha="center", transform=ax.transAxes, fontsize=8.5, color=MUTED)

save("chart9_growth_signals.png")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 10 — Gantt
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(13, 7))
fig.subplots_adjust(left=0.34, right=0.98, top=0.90, bottom=0.09)

tasks = [
    ("Shadow DevRel · Eng · Billing · DS",          1,  7,  SUBTLE,   0),
    ("Build live funnel dashboard",                   1,  14, SUBTLE,   0),
    ("12 developer interviews (4 segments)",          8,  7,  BLUE,     0),
    ("Session replay audit + competitor onboarding",  8,  7,  BLUE,     0),
    ("Funnel data deep dive + thesis selection",      15, 7,  C_GOOGLE, 0),
    ("Stakeholder alignment + 30-day Loom readout",   22, 8,  C_GOOGLE, 0),
    ("E1: In-console quickstart  (A/B live)",         31, 21, GREEN,    1),
    ("E2: Contextual upgrade CTA  (A/B live)",        31, 28, ORANGE,   1),
    ("E3: Claude Code→API  (validate assumption)",    31, 7,  BLUE,     1),
    ("E3: Build + instrument  (if <40% converted)",   38, 21, BLUE,     1),
    ("Kill review — stop no-signal experiments",      52, 3,  "#b91c1c", 1),
    ("Scale E1 winner → docs + SDKs",                61, 20, GREEN,    2),
    ("Scale E2 winner → all limit surfaces",          61, 20, ORANGE,   2),
    ("Draft + socialise platform thesis",             61, 14, SUBTLE,   2),
    ("Present platform thesis to leadership",         85, 5,  C_GOOGLE, 2),
]

phase_bg = {0: "#edf4fb", 1: "#fdf5f0", 2: "#f0f7ec"}
for ph, (s, e) in {0: (1, 30), 1: (31, 60), 2: (61, 90)}.items():
    ax.axvspan(s, e, alpha=0.35, color=phase_bg[ph], zorder=0)

for i, (label, start, dur, clr, ph) in enumerate(tasks):
    ax.barh(i, dur, left=start, height=0.55, color=clr, alpha=0.88, zorder=2)

ax.set_yticks(range(len(tasks)))
ax.set_yticklabels([t[0] for t in tasks], fontsize=9.5)
ax.set_xlim(0, 93)
ax.set_xlabel("Day")
ax.set_title("30-60-90 Day Plan — Task Timeline", color=TEXT)
ax.xaxis.grid(True, color=BORDER, zorder=1, alpha=0.7); ax.set_axisbelow(True)

for day in [1, 30, 31, 60, 61, 90]:
    ax.axvline(day, color=SUBTLE, lw=0.9, ls="--", alpha=0.7, zorder=3)

phase_names = {0: "Days 1–30\nListen", 1: "Days 31–60\nExperiment", 2: "Days 61–90\nExecute"}
for ph, (s, e) in {0: (1, 30), 1: (31, 60), 2: (61, 90)}.items():
    ax.text((s+e)/2, len(tasks) + 0.05, phase_names[ph],
            ha="center", va="bottom", fontsize=9, fontweight="bold",
            color=TEXT, linespacing=1.4)

save("chart10_gantt.png")

print("\nAll 10 charts regenerated.")
