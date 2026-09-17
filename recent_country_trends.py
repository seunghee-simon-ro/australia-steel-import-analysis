import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


# ======================================
# AUSTRALIA STEEL IMPORT
# RECENT COUNTRY TRENDS
# ======================================

print("======================================")
print(" AUSTRALIA STEEL IMPORT")
print(" RECENT COUNTRY TRENDS")
print("======================================")


# ======================================
# 1. LOAD DATA
# ======================================

df = pd.read_csv(
    "long_term_country_analysis.csv"
)

df["YEAR"] = df["YEAR"].astype(int)


# ======================================
# 2. COUNTRIES
# ======================================

main_countries = [
    "China",
    "Japan",
    "South Korea",
    "Taiwan",
    "India",
    "Indonesia",
    "Malaysia"
]


# ======================================
# 3. IMPORT VALUE TREND
# ======================================

trend = df[
    df["COUNTRY_NAME"].isin(
        main_countries
    )
].copy()


# ======================================
# 4. GRAPH 1
# IMPORT VALUE
# ======================================

plt.figure(
    figsize=(14, 8)
)

for country in main_countries:

    country_data = trend[
        trend["COUNTRY_NAME"] == country
    ]

    plt.plot(
        country_data["YEAR"],
        country_data[
            "IMPORT_VALUE_BILLION_AUD"
        ],
        marker="o",
        linewidth=2,
        label=country
    )


plt.title(
    "Australia Steel Import Value by Country",
    fontsize=18
)

plt.xlabel(
    "Year",
    fontsize=12
)

plt.ylabel(
    "Import Value (AUD Billion)",
    fontsize=12
)

plt.xticks(
    range(
        2015,
        2027
    ),
    rotation=45
)

plt.grid(
    True,
    alpha=0.3
)

plt.legend()

plt.tight_layout()


plt.savefig(
    "recent_country_import_trends.png",
    dpi=300,
    bbox_inches="tight"
)


print(
    "Saved: recent_country_import_trends.png"
)


# ======================================
# 5. SOUTH KOREA MARKET SHARE
# ======================================

korea = trend[
    trend["COUNTRY_NAME"]
    == "South Korea"
].copy()


# ======================================
# GRAPH 2
# ======================================

plt.figure(
    figsize=(14, 8)
)

plt.plot(
    korea["YEAR"],
    korea["MARKET_SHARE_%"],
    marker="o",
    linewidth=3
)


plt.title(
    "South Korea Steel Import Market Share in Australia",
    fontsize=18
)

plt.xlabel(
    "Year",
    fontsize=12
)

plt.ylabel(
    "Market Share (%)",
    fontsize=12
)

plt.xticks(
    range(
        2015,
        2027
    ),
    rotation=45
)

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()


plt.savefig(
    "south_korea_market_share_trend.png",
    dpi=300,
    bbox_inches="tight"
)


print(
    "Saved: south_korea_market_share_trend.png"
)


# ======================================
# 6. MARKET SHARE COMPARISON
# ======================================

comparison_countries = [
    "China",
    "Japan",
    "South Korea",
    "Taiwan"
]


comparison = trend[
    trend["COUNTRY_NAME"].isin(
        comparison_countries
    )
].copy()


# ======================================
# GRAPH 3
# ======================================

plt.figure(
    figsize=(14, 8)
)


for country in comparison_countries:

    country_data = comparison[
        comparison["COUNTRY_NAME"]
        == country
    ]

    plt.plot(
        country_data["YEAR"],
        country_data[
            "MARKET_SHARE_%"
        ],
        marker="o",
        linewidth=2.5,
        label=country
    )


plt.title(
    "Steel Import Market Share in Australia",
    fontsize=18
)

plt.xlabel(
    "Year",
    fontsize=12
)

plt.ylabel(
    "Market Share (%)",
    fontsize=12
)

plt.xticks(
    range(
        2015,
        2027
    ),
    rotation=45
)

plt.grid(
    True,
    alpha=0.3
)

plt.legend()

plt.tight_layout()


plt.savefig(
    "major_countries_market_share_trend.png",
    dpi=300,
    bbox_inches="tight"
)


print(
    "Saved: major_countries_market_share_trend.png"
)


# ======================================
# 7. EXPORT KOREA DATA
# ======================================

korea[
    [
        "YEAR",
        "IMPORT_VALUE_BILLION_AUD",
        "MARKET_SHARE_%",
        "YOY_GROWTH_%"
    ]
].to_csv(
    "south_korea_long_term_trend.csv",
    index=False
)


print(
    "Saved: south_korea_long_term_trend.csv"
)


# ======================================
# 8. COMPLETE
# ======================================

print("\n======================================")
print(" COUNTRY TREND ANALYSIS COMPLETE")
print("======================================")

print("\nGenerated files:")

print(
    "1. recent_country_import_trends.png"
)

print(
    "2. south_korea_market_share_trend.png"
)

print(
    "3. major_countries_market_share_trend.png"
)

print(
    "4. south_korea_long_term_trend.csv"
)

print("\n======================================")
