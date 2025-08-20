# chart.py
# Seaborn lineplot for Monthly Revenue Trend Analysis
# Requirements: seaborn, matplotlib, pandas, numpy

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ----- Synthetic business data -----
rng = np.random.default_rng(42)

months = pd.date_range("2024-01-01", periods=12, freq="MS")
segments = [
    ("Enterprise", 120_000, 0.08, 0.004, 0.0),   # (name, base, season_amp, monthly_growth, phase)
    ("SMB",         75_000, 0.12, 0.006, 0.3),
    ("Consumer",    90_000, 0.18, 0.008, 0.6),
]

records = []
for s_name, base, amp, g, phase in segments:
    for i, m in enumerate(months):
        # seasonal multiplier: 1 + amp*sin(2π * month/12 + phase)
        season = 1.0 + amp * np.sin(2 * np.pi * (i / 12) + phase)
        # growth multiplier: compounding month-over-month
        growth = (1.0 + g) ** i
        # noise at ~5% of base
        noise = rng.normal(0, 0.05 * base)
        revenue = base * season * growth + noise
        records.append({"month": m, "segment": s_name, "revenue": revenue})

df = pd.DataFrame(records)

# ----- Seaborn styling -----
sns.set_style("whitegrid")
sns.set_context("talk", font_scale=0.9)

# EXACT 512×512 px: 8 in × 8 in at 64 dpi
plt.figure(figsize=(8, 8))

ax = sns.lineplot(
    data=df,
    x="month",
    y="revenue",
    hue="segment",
    marker="o",
    linewidth=2
)

ax.set_title("Monthly Revenue by Customer Segment (Synthetic)")
ax.set_xlabel("Month (2024)")
ax.set_ylabel("Revenue (USD)")
ax.legend(title="Segment", loc="upper left", frameon=True)

# Slightly nicer x ticks
ax.xaxis.set_major_locator(plt.MaxNLocator(6))
plt.tight_layout()

# EXACT size by spec
plt.savefig("chart.png", dpi=64, bbox_inches="tight")
