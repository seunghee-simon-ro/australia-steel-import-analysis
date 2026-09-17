import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


# ======================================
# AUSTRALIA STEEL IMPORT
# MARKET SHARE ANALYSIS
# ======================================

print("======================================")
print(" AUSTRALIA STEEL IMPORT")
print(" MARKET SHARE ANALYSIS")
print("======================================")


# ======================================
# 1. LOAD DATA
# ======================================

df = pd.read_csv("steel_import_raw.csv")

df["TIME_PERIOD"] = pd.to_datetime(
    df["TIME_PERIOD"]
)

# UNIT_MULT = 3 → thousand AUD
df["OBS_VALUE_AUD"] = (
    df["OBS_VALUE"] * 1000
)


# ======================================
# 2. REMOVE TOTAL
# ======================================

df = df[
    df["COUNTRY_ORIGIN"] != "TOT"
]


# ======================================
# 3. COUNTRY NAME
# ======================================

country_names = {

    "NCD": "No Country Details",

    "CHIN": "China",
    "JAP": "Japan",
    "TAIW": "Taiwan",
    "INIA": "India",
    "RKOR": "South Korea",
    "INDO": "Indonesia",
    "FGMY": "Germany",
    "USA": "United States",
    "MLAY": "Malaysia",

    "SWED": "Sweden",
    "VIET": "Vietnam",
    "SING": "Singapore",
    "ITAL": "Italy",
    "CAN": "Canada",
    "UK": "United Kingdom",
    "FRAN": "France",
    "NETH": "Netherlands",
    "BRAZ": "Brazil",
    "RUSS": "Russia",
    "THAI": "Thailand",
    "SAFR": "South Africa",
    "BELG": "Belgium",
    "SPAI": "Spain",
    "MEXI": "Mexico",
    "NZ": "New Zealand",
    "HONG": "Hong Kong",
    "TURK": "Turkey",
    "SWIT": "Switzerland",
    "POLA": "Poland",
    "CZEH": "Czech Republic",
    "PHIL": "Philippines",
    "PAKI": "Pakistan",
    "SAUD": "Saudi Arabia",
    "UAE": "United Arab Emirates",
}


df["COUNTRY_NAME"] = (
    df["COUNTRY_ORIGIN"]
    .map(country_names)
    .fillna(df["COUNTRY_ORIGIN"])
)


# ======================================
# 4. TOTAL MARKET BY YEAR
# ======================================

df["YEAR"] = (
    df["TIME_PERIOD"].dt.year
)

annual_total = (
    df.groupby("YEAR")["OBS_VALUE_AUD"]
    .sum()
    .reset_index()
)


annual_total["TOTAL_IMPORT_BILLION_AUD"] = (
    annual_total["OBS_VALUE_AUD"]
    / 1_000_000_000
)


# ======================================
# 5. COUNTRY IMPORT BY YEAR
# ======================================

country_annual = (
    df.groupby(
        ["YEAR", "COUNTRY_NAME"]
    )["OBS_VALUE_AUD"]
    .sum()
    .reset_index()
)


# ======================================
# 6. MERGE WITH TOTAL MARKET
# ======================================

country_annual = country_annual.merge(
    annual_total[
        [
            "YEAR",
            "OBS_VALUE_AUD"
        ]
    ],
    on="YEAR",
    suffixes=(
        "_COUNTRY",
        "_TOTAL"
    )
)


# ======================================
# 7. MARKET SHARE
# ======================================

country_annual["MARKET_SHARE_%"] = (
    country_annual["OBS_VALUE_AUD_COUNTRY"]
    /
    country_annual["OBS_VALUE_AUD_TOTAL"]
    * 100
)


country_annual[
    "IMPORT_VALUE_BILLION_AUD"
] = (
    country_annual["OBS_VALUE_AUD_COUNTRY"]
    / 1_000_000_000
)


# ======================================
# 8. RECENT YEARS
# ======================================

recent = country_annual[
    country_annual["YEAR"].isin(
        [2024, 2025, 2026]
    )
].copy()


# ======================================
# 9. 2024 / 2025 FULL YEAR
# 2026 = YTD
# ======================================

print("\n======================================")
print(" 2024 / 2025 / 2026 YTD")
print("======================================")


for year in [2024, 2025, 2026]:

    temp = recent[
        recent["YEAR"] == year
    ].sort_values(
        "IMPORT_VALUE_BILLION_AUD",
        ascending=False
    )

    print(
        f"\n--- {year} ---"
    )

    print(
        temp[
            [
                "COUNTRY_NAME",
                "IMPORT_VALUE_BILLION_AUD",
                "MARKET_SHARE_%"
            ]
        ]
        .head(15)
        .round(2)
        .to_string(index=False)
    )


# ======================================
# 10. TOP COUNTRIES — 2025
# ======================================

top_2025 = (
    recent[
        recent["YEAR"] == 2025
    ]
    .sort_values(
        "IMPORT_VALUE_BILLION_AUD",
        ascending=False
    )
    .head(15)
)


print("\n======================================")
print(" TOP 15 COUNTRIES — 2025")
print("======================================")

print(
    top_2025[
        [
            "COUNTRY_NAME",
            "IMPORT_VALUE_BILLION_AUD",
            "MARKET_SHARE_%"
        ]
    ]
    .round(2)
    .to_string(index=False)
)


# ======================================
# 11. SOUTH KOREA
# ======================================

korea = country_annual[
    country_annual["COUNTRY_NAME"]
    == "South Korea"
].copy()


print("\n======================================")
print(" SOUTH KOREA")
print("======================================")


print(
    korea[
        [
            "YEAR",
            "IMPORT_VALUE_BILLION_AUD",
            "MARKET_SHARE_%"
        ]
    ]
    .round(3)
    .to_string(index=False)
)


# ======================================
# 12. 2025 MARKET SHARE GRAPH
# ======================================

plt.figure(
    figsize=(14, 9)
)


top_2025_plot = (
    top_2025
    .sort_values(
        "MARKET_SHARE_%",
        ascending=True
    )
)


plt.barh(
    top_2025_plot["COUNTRY_NAME"],
    top_2025_plot["MARKET_SHARE_%"]
)


plt.title(
    "Australia Steel Import Market Share — 2025",
    fontsize=18
)

plt.xlabel(
    "Market Share (%)",
    fontsize=12
)

plt.ylabel(
    "Country",
    fontsize=12
)

plt.grid(
    axis="x",
    alpha=0.3
)

plt.tight_layout()


# ======================================
# 13. KOREA MARKET SHARE TREND
# ======================================

plt.figure(
    figsize=(14, 7)
)


plt.plot(
    korea["YEAR"],
    korea["MARKET_SHARE_%"],
    marker="o"
)


plt.title(
    "South Korea — Australia Steel Import Market Share",
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

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()


# ======================================
# 14. SAVE DATA
# ======================================

country_annual.to_csv(
    "steel_import_market_share.csv",
    index=False
)


recent.to_csv(
    "steel_import_recent_market_share.csv",
    index=False
)


print("\n======================================")
print(" ANALYSIS COMPLETE")
print("======================================")

print("\nSaved:")

print(
    "steel_import_market_share.csv"
)

print(
    "steel_import_recent_market_share.csv"
)


# ======================================
# SHOW GRAPHS
# ======================================

plt.show()