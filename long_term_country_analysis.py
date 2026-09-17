import pandas as pd


# ======================================
# AUSTRALIA STEEL IMPORT
# LONG-TERM COUNTRY ANALYSIS
# ======================================

print("======================================")
print(" AUSTRALIA STEEL IMPORT")
print(" LONG-TERM COUNTRY ANALYSIS")
print("======================================")


# ======================================
# 1. LOAD DATA
# ======================================

df = pd.read_csv("steel_import_raw.csv")

df["TIME_PERIOD"] = pd.to_datetime(
    df["TIME_PERIOD"]
)

# UNIT_MULT = 3
# Values are thousand AUD
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
# 5. MAIN COUNTRIES
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
# 6. MAIN COUNTRY DATA
# ======================================

main_df = df[
    df["COUNTRY_NAME"].isin(
        main_countries
    )
].copy()


# ======================================
# 7. ANNUAL IMPORT VALUE
# ======================================

annual_country = (

    main_df
    .groupby(
        [
            "YEAR",
            "COUNTRY_NAME"
        ]
    )["OBS_VALUE_AUD"]
    .sum()
    .reset_index()

)


annual_country[
    "IMPORT_VALUE_BILLION_AUD"
] = (
    annual_country["OBS_VALUE_AUD"]
    / 1_000_000_000
)


# ======================================
# 8. TOTAL AUSTRALIA MARKET
# ======================================

annual_market = (

    df
    .groupby("YEAR")
    ["OBS_VALUE_AUD"]
    .sum()
    .reset_index()

)


annual_market[
    "TOTAL_MARKET_BILLION_AUD"
] = (
    annual_market["OBS_VALUE_AUD"]
    / 1_000_000_000
)


# ======================================
# 9. MARKET SHARE
# ======================================

annual_country = annual_country.merge(

    annual_market[
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


annual_country[
    "MARKET_SHARE_%"
] = (

    annual_country[
        "OBS_VALUE_AUD_COUNTRY"
    ]

    /

    annual_country[
        "OBS_VALUE_AUD_MARKET"
    ]

    * 100

)


# ======================================
# 10. YEAR-ON-YEAR GROWTH
# ======================================

annual_country = (
    annual_country
    .sort_values(
        [
            "COUNTRY_NAME",
            "YEAR"
        ]
    )
)


annual_country[
    "YOY_GROWTH_%"
] = (

    annual_country
    .groupby("COUNTRY_NAME")
    [
        "IMPORT_VALUE_BILLION_AUD"
    ]
    .pct_change()
    * 100

)


# ======================================
# 11. PIVOT — IMPORT VALUE
# ======================================

value_pivot = (

    annual_country
    .pivot(
        index="YEAR",
        columns="COUNTRY_NAME",
        values="IMPORT_VALUE_BILLION_AUD"
    )

)


# ======================================
# 12. PIVOT — MARKET SHARE
# ======================================

share_pivot = (

    annual_country
    .pivot(
        index="YEAR",
        columns="COUNTRY_NAME",
        values="MARKET_SHARE_%"
    )

)


# ======================================
# 13. PRINT LONG-TERM IMPORT VALUE
# ======================================

print("\n======================================")
print(" IMPORT VALUE — AUD BILLION")
print("======================================")

print(
    value_pivot
    .round(3)
    .to_string()
)


# ======================================
# 14. PRINT MARKET SHARE
# ======================================

print("\n======================================")
print(" MARKET SHARE — %")
print("======================================")

print(
    share_pivot
    .round(2)
    .to_string()
)


# ======================================
# 15. SOUTH KOREA ANALYSIS
# ======================================

korea = annual_country[
    annual_country["COUNTRY_NAME"]
    == "South Korea"
].copy()


print("\n======================================")
print(" SOUTH KOREA — LONG TERM")
print("======================================")


print(

    korea[
        [
            "YEAR",
            "IMPORT_VALUE_BILLION_AUD",
            "MARKET_SHARE_%",
            "YOY_GROWTH_%"
        ]
    ]

    .round(2)

    .to_string(
        index=False
    )

)


# ======================================
# 16. 2015 VS 2025
# ======================================

korea_2015 = korea[
    korea["YEAR"] == 2015
]


korea_2025 = korea[
    korea["YEAR"] == 2025
]


if not korea_2015.empty and not korea_2025.empty:

    value_2015 = (
        korea_2015[
            "IMPORT_VALUE_BILLION_AUD"
        ].iloc[0]
    )

    value_2025 = (
        korea_2025[
            "IMPORT_VALUE_BILLION_AUD"
        ].iloc[0]
    )

    share_2015 = (
        korea_2015[
            "MARKET_SHARE_%"
        ].iloc[0]
    )

    share_2025 = (
        korea_2025[
            "MARKET_SHARE_%"
        ].iloc[0]
    )

    print("\n--------------------------------------")
    print(" SOUTH KOREA: 2015 → 2025")
    print("--------------------------------------")

    print(
        f"Import value 2015: "
        f"{value_2015:.3f} billion AUD"
    )

    print(
        f"Import value 2025: "
        f"{value_2025:.3f} billion AUD"
    )

    print(
        f"Market share 2015: "
        f"{share_2015:.2f}%"
    )

    print(
        f"Market share 2025: "
        f"{share_2025:.2f}%"
    )

    print(
        f"Import value change: "
        f"{(value_2025 / value_2015 - 1) * 100:.2f}%"
    )

    print(
        f"Market share change: "
        f"{share_2025 - share_2015:+.2f} percentage points"
    )


# ======================================
# 17. 2025 RANKING
# ======================================

ranking_2025 = (

    annual_country[
        annual_country["YEAR"] == 2025
    ]

    .sort_values(
        "IMPORT_VALUE_BILLION_AUD",
        ascending=False
    )

)


ranking_2025[
    "RANK_2025"
] = range(
    1,
    len(ranking_2025) + 1
)


print("\n======================================")
print(" 2025 MAJOR COUNTRY RANKING")
print("======================================")


print(

    ranking_2025[
        [
            "RANK_2025",
            "COUNTRY_NAME",
            "IMPORT_VALUE_BILLION_AUD",
            "MARKET_SHARE_%"
        ]
    ]

    .round(2)

    .to_string(
        index=False
    )

)


# ======================================
# 18. 2026 YTD
# ======================================

ytd_2026 = annual_country[
    annual_country["YEAR"] == 2026
].copy()


print("\n======================================")
print(" 2026 YTD")
print("======================================")

print(
    ytd_2026[
        [
            "COUNTRY_NAME",
            "IMPORT_VALUE_BILLION_AUD",
            "MARKET_SHARE_%"
        ]
    ]

    .sort_values(
        "IMPORT_VALUE_BILLION_AUD",
        ascending=False
    )

    .round(2)

    .to_string(
        index=False
    )
)


# ======================================
# 19. SAVE MAIN DATA
# ======================================

annual_country.to_csv(
    "long_term_country_analysis.csv",
    index=False
)


# ======================================
# 20. SAVE IMPORT VALUE PIVOT
# ======================================

value_pivot.to_csv(
    "long_term_import_value.csv"
)


# ======================================
# 21. SAVE MARKET SHARE PIVOT
# ======================================

share_pivot.to_csv(
    "long_term_market_share.csv"
)


# ======================================
# 22. SAVE 2025 RANKING
# ======================================

ranking_2025.to_csv(
    "2025_country_ranking.csv",
    index=False
)


# ======================================
# 23. SAVE 2026 YTD
# ======================================

ytd_2026.to_csv(
    "2026_country_ytd.csv",
    index=False
)


# ======================================
# COMPLETE
# ======================================

print("\n======================================")
print(" LONG-TERM ANALYSIS COMPLETE")
print("======================================")

print("\nSaved files:")

print(
    "long_term_country_analysis.csv"
)

print(
    "long_term_import_value.csv"
)

print(
    "long_term_market_share.csv"
)

print(
    "2025_country_ranking.csv"
)

print(
    "2026_country_ytd.csv"
)

print("\n======================================")
