import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np

# ── Style ──────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "figure.facecolor": "#FAFAFA",
    "axes.facecolor": "#FAFAFA",
})
COLORS = {
    "anthropic": "#C25B2D",
    "openai":    "#10A37F",
    "google":    "#4285F4",
    "microsoft": "#0078D4",
    "aws":       "#FF9900",
    "cohere":    "#8B5CF6",
    "meta":      "#1877F2",
    "neutral":   "#94A3B8",
    "warn":      "#F59E0B",
    "ok":        "#22C55E",
}

OUT = "/Users/gztd-03-02619/Q2/the_future/"

# ══════════════════════════════════════════════════════════════════════════════
# Chart 1 — ARR Comparison (with dispute annotation)
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 3.5))
companies = ["Anthropic\n(gross-reported)", "OpenAI", "Anthropic\n(disputed net)"]
arr = [30, 25, 22]
clrs = [COLORS["anthropic"], COLORS["openai"], COLORS["anthropic"]]
alphas = [1.0, 1.0, 0.45]
bars = []
for comp, val, clr, al in zip(companies, arr, clrs, alphas):
    b = ax.barh(comp, val, color=clr, alpha=al, height=0.5)
    bars.append(b[0])
ax.set_xlabel("ARR ($B, April 2026)")
ax.set_title("ARR Comparison: Anthropic vs OpenAI")
for bar, val in zip(bars, arr):
    ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
            f"${val}B", va="center", fontweight="bold")
ax.axvline(22, color=COLORS["anthropic"], ls="--", alpha=0.4, lw=1)
ax.set_xlim(0, 36)
note = mpatches.Patch(color=COLORS["anthropic"], alpha=0.45, label="~$8B dispute (gross vs. net on AWS/GCP deals)")
ax.legend(handles=[note], fontsize=8, loc="lower right")
ax.set_facecolor("#FAFAFA")
caption = "Anthropic leads on gross-reported ARR; OpenAI disputes ~$8B via revenue recognition.\nUnderlying growth trajectory (70× API YoY) is not in dispute."
fig.text(0.5, -0.04, caption, ha="center", fontsize=8, color="#64748B")
plt.tight_layout()
plt.savefig(OUT + "chart1_arr_comparison.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 1 done")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 2 — Developer Community Scale
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 4))
labels = ["OpenAI", "Google\nGemini", "GitHub\n(MSFT)", "AWS\nBedrock", "Cohere\n(enterprise)", "Anthropic\n(self-serve)"]
devs = [4_000_000, 2_400_000, 145_000_000, 100_000, 17_000, None]
bar_clrs = [COLORS["openai"], COLORS["google"], COLORS["microsoft"], COLORS["aws"], COLORS["cohere"], COLORS["anthropic"]]
# GitHub is so large it distorts; normalize to log-scale intuition, show separately
main_labels = ["OpenAI", "Google\nGemini", "AWS\nBedrock", "Cohere\n(enterprise)"]
main_devs   = [4_000_000, 2_400_000, 100_000, 17_000]
main_clrs   = [COLORS["openai"], COLORS["google"], COLORS["aws"], COLORS["cohere"]]

bars = ax.bar(main_labels, main_devs, color=main_clrs, width=0.55)
for bar, val in zip(bars, main_devs):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 40_000,
            f"{val/1_000_000:.1f}M" if val >= 1_000_000 else f"{val:,}",
            ha="center", fontsize=9, fontweight="bold")

ax.set_ylabel("Active Developers / Organizations")
ax.set_title("API Developer Community Scale (May 2026)\n[GitHub/145M excluded — different measure]")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x/1_000_000:.1f}M" if x >= 1_000_000 else f"{int(x/1000)}K"))
ax.text(0, -380_000, "Anthropic: community size not publicly disclosed; 70× API volume YoY signals intensity, not breadth.",
        fontsize=8, color="#64748B")
plt.tight_layout()
plt.savefig(OUT + "chart2_developer_scale.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 2 done")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 3 — RICE Priority: Channels & Experiments
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

# 3a: Channels
ch_labels = ["Docs /\nRunnable Samples", "Claude Code\n→ API On-ramp", "Bedrock\nIncrementality", "Developer\nCommunity"]
ch_scores = [52_500, 16_250, 0, 625]
ch_reco   = ["Scale", "Scale", "Research", "Build (6–12mo)"]
ch_clrs   = [COLORS["ok"], COLORS["anthropic"], COLORS["warn"], COLORS["neutral"]]
b = axes[0].bar(ch_labels, ch_scores, color=ch_clrs, width=0.55)
axes[0].set_title("Acquisition Channels — RICE Score")
axes[0].set_ylabel("RICE Score")
for bar, score, rec in zip(b, ch_scores, ch_reco):
    if score > 0:
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
                     f"{score:,}\n({rec})", ha="center", fontsize=8.5, fontweight="bold")
    else:
        axes[0].text(bar.get_x() + bar.get_width()/2, 800, "(Research)", ha="center", fontsize=8, color="#64748B")

# 3b: Experiments
exp_labels = ["E1: In-console\nQuickstart", "E2: Contextual\nUpgrade CTA", "E3: Claude Code\n→ API Path"]
exp_scores = [52_500, 14_625, 15_000]
exp_notes  = ["#1 Priority\n(2 weeks)", "#2 Priority\n(2 weeks)", "#3 Priority\n(validate first)"]
exp_clrs   = [COLORS["ok"], COLORS["anthropic"], COLORS["warn"]]
b2 = axes[1].bar(exp_labels, exp_scores, color=exp_clrs, width=0.55)
axes[1].set_title("Days 31–60 Experiments — RICE Score")
for bar, score, note in zip(b2, exp_scores, exp_notes):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 400,
                 f"{score:,}\n{note}", ha="center", fontsize=8.5, fontweight="bold")

fig.text(0.5, -0.04, "RICE = (Reach × Impact × Confidence) / Effort (person-weeks). E3 requires assumption validation before build.",
         ha="center", fontsize=8, color="#64748B")
plt.tight_layout()
plt.savefig(OUT + "chart3_rice_scores.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 3 done")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 4 — OST Recommended POC Scores
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 4))
pocs = ["A1: In-console\nInteractive Quickstart", "B1: Contextual\nUpgrade Modal", "C1: Claude Code\n→ API On-ramp"]
feasibility = [4, 4, 3]
impact      = [4, 5, 3]
market_fit  = [5, 5, 4]
totals      = [f+i+m for f, i, m in zip(feasibility, impact, market_fit)]

x = np.arange(len(pocs))
w = 0.22
b1 = ax.bar(x - w, feasibility, w, label="Feasibility (1–5)", color=COLORS["ok"])
b2 = ax.bar(x,     impact,      w, label="Impact (1–5)",      color=COLORS["anthropic"])
b3 = ax.bar(x + w, market_fit,  w, label="Market Fit (1–5)",  color=COLORS["google"])

for xi, total in zip(x, totals):
    ax.text(xi, 5.5, f"Total: {total}/15", ha="center", fontweight="bold", fontsize=9,
            color="#1E293B")

ax.set_xticks(x)
ax.set_xticklabels(pocs)
ax.set_ylim(0, 6.5)
ax.set_ylabel("Score (1–5)")
ax.set_title("OST Recommended POCs — Scoring")
ax.legend(loc="upper right", fontsize=8)
note = "C1 requires validating assumption first: what % of Claude Code users are already API users?\nIf >80% already converted → redirect effort to expansion, not conversion."
ax.text(0.5, -0.18, note, ha="center", transform=ax.transAxes, fontsize=8, color="#64748B")
plt.tight_layout()
plt.savefig(OUT + "chart4_ost_scores.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 4 done")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 5 — Competitor Positioning Matrix (Price vs Safety)
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7.5, 5.5))
# x = relative price (lower = cheaper), y = safety architecture depth
# normalized 1-10 scales (qualitative)
comp_data = {
    "Meta Llama\n(free/OSS)":  (1, 3,  COLORS["meta"],      300),
    "Google\nGemini":          (2, 4,  COLORS["google"],     350),
    "AWS\nBedrock":            (4, 5,  COLORS["aws"],        300),
    "Microsoft\nAzure AI":     (5, 6,  COLORS["microsoft"],  300),
    "OpenAI\nAPI":             (7, 5,  COLORS["openai"],     300),
    "Cohere":                  (6, 7,  COLORS["cohere"],     200),
    "Anthropic\nClaude":       (6, 9,  COLORS["anthropic"],  400),
}
for label, (px, py, clr, sz) in comp_data.items():
    ax.scatter(px, py, s=sz, color=clr, alpha=0.85, zorder=3, edgecolors="white", linewidths=1.5)
    offset_x = 0.15 if label != "OpenAI\nAPI" else -1.1
    offset_y = 0.25 if label not in ("AWS\nBedrock", "Cohere") else -0.5
    ax.text(px + offset_x, py + offset_y, label, fontsize=8.5, va="center", color="#1E293B")

ax.set_xlim(0, 11)
ax.set_ylim(0, 11)
ax.set_xlabel("← Cheaper        Relative Price Tier        More Expensive →", labelpad=8)
ax.set_ylabel("← Marketing claim        Safety Architecture Depth        Verifiable →", labelpad=8)
ax.set_title("Competitor Positioning: Price vs. Safety Architecture Depth")
ax.axhline(7, ls="--", color="#94A3B8", alpha=0.5, lw=1)
ax.axvline(5, ls="--", color="#94A3B8", alpha=0.5, lw=1)
ax.text(0.5, 7.2, "Regulated-industry threshold", fontsize=7.5, color="#94A3B8")
ax.text(1, 0.5, "Open-source floor\n(Meta sets pricing ceiling for\ncommodity segment)", fontsize=7.5, color="#64748B")
ax.text(6.5, 9.5, "← Anthropic's\ntarget zone", fontsize=8, color=COLORS["anthropic"], fontweight="bold")
plt.tight_layout()
plt.savefig(OUT + "chart5_competitor_matrix.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 5 done")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 6 — Business Health Scorecard
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.axis("off")
dims   = ["Growth & Retention", "Unit Economics", "Capital Efficiency", "Strategic Position"]
status = ["[OK] EXCEPTIONAL\n70x API YoY; $1M+ accts 12->500+",
          "[!] MUST BASELINE\nCAC/LTV not instrumented for self-serve",
          "[!] WATCH\n$380B valuation; revenue dispute adds noise",
          "[OK] STRONG (gaps exist)\nMCP moat, Conway; community breadth lags"]
colors_row = [COLORS["ok"], COLORS["warn"], COLORS["warn"], COLORS["ok"]]

table_data = [[d, s] for d, s in zip(dims, status)]
col_labels = ["Dimension", "API Platform Status"]
tbl = ax.table(cellText=table_data, colLabels=col_labels,
               loc="center", cellLoc="left")
tbl.auto_set_font_size(False)
tbl.set_fontsize(9)
tbl.scale(1, 2.6)
for (row, col), cell in tbl.get_celld().items():
    cell.set_edgecolor("#E2E8F0")
    if row == 0:
        cell.set_facecolor("#1E293B")
        cell.get_text().set_color("white")
        cell.get_text().set_fontweight("bold")
    elif col == 1 and row > 0:
        cell.set_facecolor(colors_row[row-1] + "22")
    else:
        cell.set_facecolor("#FAFAFA")
ax.set_title("Business Health Scorecard — Claude Platform API", fontweight="bold", pad=12, y=0.98)
fig.text(0.5, 0.01, "Overall verdict: Strong Growth, Underbuilt Self-Serve. Fix the funnel — the economics are already good.",
         ha="center", fontsize=8, color="#64748B")
plt.tight_layout()
plt.savefig(OUT + "chart6_health_scorecard.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 6 done")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 7 — Risk Matrix (Likelihood × Impact)
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 6))
# (likelihood 1=Low 2=Med 3=High, impact 1=Low 2=Med 3=High)
risks = [
    ("Model releases\ninvalidate experiments",     3, 2),
    ("Eng capacity\nconsumed by infra",            3, 3),
    ("Meta Llama free tier\npulls cost-sensitive", 3, 3),
    ("Google $2/M pricing\npressure",              2, 3),
    ("Revenue accounting\nmetric noise",           1, 2),
    ("Claude Code→API\nassumption invalid",        2, 2),
    ("Bedrock channel\nconflict",                  2, 2),
    ("Enterprise expansion\nblocked by procurement", 2, 3),
]
jitter = np.random.default_rng(42)
for label, lkh, imp in risks:
    jx = lkh + jitter.uniform(-0.12, 0.12)
    jy = imp  + jitter.uniform(-0.12, 0.12)
    color = COLORS["anthropic"] if (lkh == 3 and imp == 3) else (COLORS["warn"] if imp == 3 or lkh == 3 else COLORS["neutral"])
    ax.scatter(jx, jy, s=280, color=color, alpha=0.75, zorder=3, edgecolors="white", lw=1.5)
    ax.annotate(label, (jx, jy), textcoords="offset points", xytext=(8, 4),
                fontsize=7.5, color="#1E293B")

ax.set_xlim(0.5, 3.7)
ax.set_ylim(0.5, 3.7)
ax.set_xticks([1, 2, 3])
ax.set_xticklabels(["Low", "Medium", "High"])
ax.set_yticks([1, 2, 3])
ax.set_yticklabels(["Low", "Medium", "High"])
ax.set_xlabel("Likelihood")
ax.set_ylabel("Impact")
ax.set_title("Risk Matrix — 30-60-90 Day Plan")
# quadrant shading
ax.fill_between([2.5, 3.7], [2.5, 2.5], [3.7, 3.7], color="#FEE2E2", alpha=0.35, zorder=0)
ax.text(3.0, 3.5, "Act now", fontsize=8, color="#DC2626", alpha=0.7)
plt.tight_layout()
plt.savefig(OUT + "chart7_risk_matrix.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 7 done")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 8 — KPI Targets Timeline
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.axis("off")
kpi_data = [
    ["New API signups/week",         "Baseline W1",           "Baseline +20%",   "Track trend"],
    ["Claude Code → API conversion", "Instrument (W1)",       "+30%",            "Full rollout if E3 wins"],
    ["TTFAC <5 min rate",            "Measure",               "≥50% of signups", "Sustain / extend to docs"],
    ["D7 retention",                 "Measure",               ">40% (PLG P75)",  "Cohort analysis"],
    ["Free → paid conversion",       "Baseline W1",           "+20%",            "Revenue attribution"],
    ["$10K→$100K ARR expansion",     "Baseline W1",           "Track rate",      "Key for Thesis B decision"],
]
col_labels = ["Metric", "Days 1–30", "Days 31–60", "Days 61–90"]
tbl = ax.table(cellText=kpi_data, colLabels=col_labels,
               loc="center", cellLoc="left")
tbl.auto_set_font_size(False)
tbl.set_fontsize(8.5)
tbl.scale(1, 2.1)
for (row, col), cell in tbl.get_celld().items():
    cell.set_edgecolor("#E2E8F0")
    if row == 0:
        cell.set_facecolor("#1E293B")
        cell.get_text().set_color("white")
        cell.get_text().set_fontweight("bold")
    elif col == 0:
        cell.set_facecolor("#F1F5F9")
    elif col == 2:
        cell.set_facecolor(COLORS["ok"] + "18")
    else:
        cell.set_facecolor("#FAFAFA")
ax.set_title("KPI Framework — Targets by Phase", fontweight="bold", y=0.98)
fig.text(0.5, 0.01, "D30 retention measurable only for cohorts from Days 1–60. E3 requires Week 1 instrumentation as prerequisite.",
         ha="center", fontsize=7.5, color="#64748B")
plt.tight_layout()
plt.savefig(OUT + "chart8_kpi_framework.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 8 done")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 9 — Claude Platform Growth Signals
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(11, 4))

# 9a: $1M+ ARR accounts
ax = axes[0]
ax.bar(["Jan 2025", "Apr 2026"], [12, 500], color=[COLORS["neutral"], COLORS["anthropic"]], width=0.5)
ax.set_title("$1M+ ARR Accounts")
ax.set_ylabel("Count")
ax.text(1, 515, "500+\n(41×)", ha="center", fontweight="bold", color=COLORS["anthropic"])
ax.text(0, 27, "12", ha="center", fontweight="bold", color="#64748B")
ax.text(0.5, -70, "41× growth in ~15 months", ha="center", fontsize=8, color="#64748B",
        transform=ax.transData)

# 9b: Claude Code business subs (index 100 = Jan 2026)
ax = axes[1]
months = ["Jan 2026", "May 2026"]
vals = [100, 400]
ax.plot(months, vals, "o-", color=COLORS["anthropic"], lw=2.5, ms=8)
ax.fill_between(months, vals, alpha=0.12, color=COLORS["anthropic"])
ax.set_title("Claude Code Business Subscriptions\n(Index: Jan 2026 = 100)")
ax.set_ylabel("Index")
ax.set_ylim(0, 450)
ax.text(1, 415, "4×", ha="center", fontweight="bold", color=COLORS["anthropic"], fontsize=13)

# 9c: Developer engagement
ax = axes[2]
platforms = ["Claude Code\n(Anthropic)", "Industry\nAverage*"]
hours = [20, 5]
clrs2 = [COLORS["anthropic"], COLORS["neutral"]]
bars = ax.bar(platforms, hours, color=clrs2, width=0.45)
ax.set_title("Developer Engagement\n(Hours/Week)")
ax.set_ylabel("Avg hrs/week")
for bar, h in zip(bars, hours):
    ax.text(bar.get_x() + bar.get_width()/2, h + 0.3, f"{h}h", ha="center", fontweight="bold")
ax.text(0.5, -3.8, "*Industry average estimated; Claude Code figure per Anthropic public disclosures.",
        ha="center", fontsize=7.5, color="#64748B", transform=ax.transData)

plt.suptitle("Anthropic Growth Signals (May 2026)", fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(OUT + "chart9_growth_signals.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 9 done")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 10 — 30-60-90 Day Gantt
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(11, 5.5))
tasks = [
    # (label, start_day, duration, color, phase)
    ("Shadow teams (DevRel, Eng, Billing, DS)",    1, 7,  COLORS["neutral"],   0),
    ("Build live funnel dashboard",                 1, 14, COLORS["neutral"],   0),
    ("Developer research sprint (12 interviews)",   8, 7,  COLORS["google"],    0),
    ("Session replay audit + competitor onboarding",8, 7,  COLORS["google"],    0),
    ("Funnel data deep dive + thesis selection",    15, 7, COLORS["openai"],    0),
    ("Stakeholder alignment + 30-day Loom readout", 22, 8, COLORS["openai"],   0),
    ("E1: In-console quickstart (A/B live)",        31, 21, COLORS["ok"],       1),
    ("E2: Contextual upgrade CTA (A/B live)",       31, 28, COLORS["anthropic"],1),
    ("E3: Claude Code→API (validate assumption)",   31, 7,  COLORS["warn"],     1),
    ("E3: Build & instrument (if assumption holds)",38, 21, COLORS["warn"],     1),
    ("Kill review — stop no-signal experiments",    52, 3,  "#DC2626",          1),
    ("Scale E1 winner → docs + SDKs",              61, 20, COLORS["ok"],       2),
    ("Scale E2 winner → all limit surfaces",        61, 20, COLORS["anthropic"],2),
    ("Draft platform thesis (A/B/C)",               61, 14, COLORS["neutral"],  2),
    ("Present platform thesis to leadership",       85, 5,  COLORS["openai"],   2),
]
yticks = []
ylabels = []
phase_labels = {0: "Days 1–30: Listen", 1: "Days 31–60: Experiment", 2: "Days 61–90: Execute"}
phase_colors = {0: "#F0F9FF", 1: "#FFF7ED", 2: "#F0FDF4"}
ax.axvspan(1,  30, alpha=0.25, color=phase_colors[0], zorder=0)
ax.axvspan(31, 60, alpha=0.25, color=phase_colors[1], zorder=0)
ax.axvspan(61, 90, alpha=0.25, color=phase_colors[2], zorder=0)
for i, (label, start, dur, clr, phase) in enumerate(tasks):
    ax.barh(i, dur, left=start, height=0.6, color=clr, alpha=0.85, zorder=2)
    yticks.append(i)
    ylabels.append(label)
ax.set_yticks(yticks)
ax.set_yticklabels(ylabels, fontsize=8.5)
ax.set_xlim(0, 92)
ax.set_xlabel("Day")
ax.set_title("30-60-90 Day Plan — Task Timeline")
for day, label in [(1, "D1"), (30, "D30"), (31, "D31"), (60, "D60"), (61, "D61"), (90, "D90")]:
    ax.axvline(day, color="#94A3B8", lw=0.7, ls="--", alpha=0.6)
for phase, (start, end) in {0: (1, 30), 1: (31, 60), 2: (61, 90)}.items():
    ax.text((start + end)/2, len(tasks) + 0.2, phase_labels[phase],
            ha="center", fontsize=8.5, fontweight="bold", color="#1E293B")
plt.tight_layout()
plt.savefig(OUT + "chart10_gantt.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 10 done")

print("\n✅ All 10 charts saved to", OUT)
