import pandas as pd
import matplotlib.pyplot as plt


# ======================================
# AUSTRALIA STEEL IMPORT
# RECENT MARKET ANALYSIS
# ======================================

print("======================================")
print(" AUSTRALIA STEEL IMPORT")
print(" RECENT MARKET ANALYSIS")
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
].copy()


# ======================================
# 3. COUNTRY NAMES
# ======================================

country_names = {

    "NCD": "No Country Details",

    "CHIN": "China",
    "JAP": "Japan",
    "RKOR": "South Korea",
    "TAIW": "Taiwan",
    "INIA": "India",
    "INDO": "Indonesia",
    "MLAY": "Malaysia",

    "FGMY": "Germany",
    "USA": "United States",
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
# 4. YEAR
# ======================================

df["YEAR"] = (
    df["TIME_PERIOD"].dt.year
)


# ======================================
# 5. SELECT MAIN COUNTRIES
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


df_main = df[
    df["COUNTRY_NAME"].isin(
        main_countries
    )
].copy()


# ======================================
# 6. RECENT YEARS
# ======================================

recent_years = [2024, 2025, 2026]

recent = df_main[
    df_main["YEAR"].isin(
        recent_years
    )
].copy()


# ======================================
# 7. COUNTRY + YEAR TOTAL
# ======================================

country_year = (
    recent
    .groupby(
        [
            "YEAR",
            "COUNTRY_NAME"
        ]
    )["OBS_VALUE_AUD"]
    .sum()
    .reset_index()
)


country_year[
    "IMPORT_VALUE_BILLION_AUD"
] = (
    country_year["OBS_VALUE_AUD"]
    / 1_000_000_000
)


# ======================================
# 8. TOTAL MARKET
# ======================================

market_year = (
    df[df["YEAR"].isin(recent_years)]
    .groupby("YEAR")["OBS_VALUE_AUD"]
    .sum()
    .reset_index()
)


market_year[
    "TOTAL_MARKET_BILLION_AUD"
] = (
    market_year["OBS_VALUE_AUD"]
    / 1_000_000_000
)


# ======================================
# 9. MARKET SHARE
# ======================================

country_year = country_year.merge(
    market_year[
        [
            "YEAR",
            "OBS_VALUE_AUD"
        ]
    ],
    on="YEAR",
    suffixes=(
        "_COUNTRY",
        "_MARKET"
    )
)


country_year[
    "MARKET_SHARE_%"
] = (
    country_year["OBS_VALUE_AUD_COUNTRY"]
    /
    country_year["OBS_VALUE_AUD_MARKET"]
    * 100
)


# ======================================
# 10. PIVOT — IMPORT VALUE
# ======================================

value_pivot = (
    country_year
    .pivot(
        index="COUNTRY_NAME",
        columns="YEAR",
        values="IMPORT_VALUE_BILLION_AUD"
    )
    .fillna(0)
)


print("\n======================================")
print(" IMPORT VALUE — AUD BILLION")
print("======================================")

print(
    value_pivot
    .round(3)
    .to_string()
)


# ======================================
# 11. PIVOT — MARKET SHARE
# ======================================

share_pivot = (
    country_year
    .pivot(
        index="COUNTRY_NAME",
        columns="YEAR",
        values="MARKET_SHARE_%"
    )
    .fillna(0)
)


print("\n======================================")
print(" MARKET SHARE — %")
print("======================================")

print(
    share_pivot
    .round(2)
    .to_string()
)


# ======================================
# 12. 2024 → 2025 CHANGE
# ======================================

change_24_25 = pd.DataFrame(
    index=main_countries
)


change_24_25["2024"] = (
    value_pivot[2024]
)


change_24_25["2025"] = (
    value_pivot[2025]
)


change_24_25["CHANGE_AUD_BILLION"] = (
    change_24_25["2025"]
    -
    change_24_25["2024"]
)


change_24_25["GROWTH_%"] = (
    (
        change_24_25["2025"]
        /
        change_24_25["2024"]
    )
    - 1
) * 100


print("\n======================================")
print(" 2024 → 2025 CHANGE")
print("======================================")

print(
    change_24_25
    .sort_values(
        "GROWTH_%",
        ascending=False
    )
    .round(2)
    .to_string()
)


# ======================================
# 13. 2025 → 2026 YTD CHANGE
# ======================================

change_25_26 = pd.DataFrame(
    index=main_countries
)


change_25_26["2025"] = (
    value_pivot[2025]
)


change_25_26["2026_YTD"] = (
    value_pivot[2026]
)


change_25_26[
    "CHANGE_AUD_BILLION"
] = (
    change_25_26["2026_YTD"]
    -
    change_25_26["2025"]
)


change_25_26["CHANGE_%"] = (
    (
        change_25_26["2026_YTD"]
        /
        change_25_26["2025"]
    )
    - 1
) * 100


print("\n======================================")
print(" 2025 → 2026 YTD")
print("======================================")

print(
    change_25_26
    .sort_values(
        "CHANGE_%",
        ascending=False
    )
    .round(2)
    .to_string()
)


# ======================================
# 14. IMPORTANT:
# 2026 IS YTD, NOT FULL YEAR
# ======================================

print("\n======================================")
print(" IMPORTANT")
print("======================================")

print(
    "2024 = Full Year"
)

print(
    "2025 = Full Year"
)

print(
    "2026 = January to July YTD"
)


# ======================================
# 15. GRAPH — 7 COUNTRIES
# ======================================

plt.figure(
    figsize=(14, 8)
)


for country in main_countries:

    data = country_year[
        country_year["COUNTRY_NAME"]
        == country
    ].sort_values("YEAR")

    plt.plot(
        data["YEAR"],
        data["IMPORT_VALUE_BILLION_AUD"],
        marker="o",
        label=country
    )


plt.title(
    "Australia Steel Imports — Major Source Countries",
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
    [2024, 2025, 2026],
    [
        "2024",
        "2025",
        "2026 YTD"
    ]
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()


# ======================================
# 16. GRAPH — MARKET SHARE
# ======================================

plt.figure(
    figsize=(14, 8)
)


for country in main_countries:

    data = country_year[
        country_year["COUNTRY_NAME"]
        == country
    ].sort_values("YEAR")

    plt.plot(
        data["YEAR"],
        data["MARKET_SHARE_%"],
        marker="o",
        label=country
    )


plt.title(
    "Australia Steel Import Market Share — Major Countries",
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
    [2024, 2025, 2026],
    [
        "2024",
        "2025",
        "2026 YTD"
    ]
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()


# ======================================
# 17. SAVE RESULTS
# ======================================

country_year.to_csv(
    "recent_country_analysis.csv",
    index=False
)


value_pivot.to_csv(
    "recent_import_value_comparison.csv"
)


share_pivot.to_csv(
    "recent_market_share_comparison.csv"
)


change_24_25.to_csv(
    "change_2024_2025.csv"
)


change_25_26.to_csv(
    "change_2025_2026_ytd.csv"
)


# ======================================
# COMPLETE
# ======================================

print("\n======================================")
print(" ANALYSIS COMPLETE")
print("======================================")

print("\nSaved files:")

print(
    "recent_country_analysis.csv"
)

print(
    "recent_import_value_comparison.csv"
)

print(
    "recent_market_share_comparison.csv"
)

print(
    "change_2024_2025.csv"
)

print(
    "change_2025_2026_ytd.csv"
)


# ======================================
# SHOW GRAPHS
# ======================================

plt.show()