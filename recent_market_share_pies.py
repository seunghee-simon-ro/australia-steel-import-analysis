import pandas as pd
import matplotlib.pyplot as plt


# ======================================
# AUSTRALIA STEEL IMPORT
# RECENT MARKET SHARE PIE CHARTS
# ======================================

print("======================================")
print(" AUSTRALIA STEEL IMPORT")
print(" RECENT MARKET SHARE PIE CHARTS")
print("======================================")


# ======================================
# 1. LOAD DATA
# ======================================

df = pd.read_csv("steel_import_raw.csv")

df["TIME_PERIOD"] = pd.to_datetime(
    df["TIME_PERIOD"]
)

# UNIT_MULT = 3
# ABS data is in thousand AUD
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
# 3. COUNTRY NAME
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
# 4. CREATE YEAR COLUMN
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
# 6. PIE CHART FUNCTION
# ======================================

def create_market_share_pie(
    year,
    title,
    filename
):

    # ------------------------------
    # Select year
    # ------------------------------

    yearly = df[
        df["YEAR"] == year
    ].copy()


    # ------------------------------
    # Total import by country
    # ------------------------------

    country_total = (

        yearly
        .groupby("COUNTRY_NAME")
        ["OBS_VALUE_AUD"]
        .sum()
        .sort_values(
            ascending=False
        )

    )


    # ------------------------------
    # Select main countries
    # ------------------------------

    top_countries = (

        country_total
        .loc[
            country_total.index.isin(
                main_countries
            )
        ]
        .sort_values(
            ascending=False
        )

    )


    # ------------------------------
    # Everything else = Others
    # ------------------------------

    others = (
        country_total.sum()
        -
        top_countries.sum()
    )


    # ------------------------------
    # Create pie data
    # ------------------------------

    pie_data = top_countries.copy()

    pie_data["Others"] = others


    # ------------------------------
    # Calculate market share
    # ------------------------------

    total_market = pie_data.sum()

    market_share = (
        pie_data
        /
        total_market
        *
        100
    )


    # ==================================
    # PRINT RESULTS
    # ==================================

    print("\n======================================")

    if year == 2026:
        print(" 2026 YTD MARKET SHARE")
    else:
        print(
            f" {year} MARKET SHARE"
        )

    print("======================================")


    for country, share in market_share.items():

        value_billion = (
            pie_data[country]
            /
            1_000_000_000
        )

        print(
            f"{country:25s}"
            f"{value_billion:8.2f}"
            f" billion AUD"
            f"  ({share:5.2f}%)"
        )


    # ==================================
    # PIE CHART
    # ==================================

    plt.figure(
        figsize=(10, 10)
    )


    plt.pie(

        pie_data,

        labels=pie_data.index,

        autopct="%1.1f%%",

        startangle=90,

        textprops={
            "fontsize": 11
        }

    )


    plt.title(
        title,
        fontsize=18,
        pad=20
    )


    plt.tight_layout()


    # ==================================
    # SAVE GRAPH
    # ==================================

    plt.savefig(

        filename,

        dpi=300,

        bbox_inches="tight"

    )


    print(
        f"\nGraph saved: {filename}"
    )


    # ==================================
    # SAVE DATA
    # ==================================

    result = pd.DataFrame({

        "COUNTRY":
            pie_data.index,

        "IMPORT_VALUE_BILLION_AUD":
            pie_data.values
            / 1_000_000_000,

        "MARKET_SHARE_%":
            market_share.values

    })


    csv_filename = (
        filename
        .replace(
            ".png",
            ".csv"
        )
    )


    result.to_csv(
        csv_filename,
        index=False
    )


    print(
        f"Data saved: {csv_filename}"
    )


# ======================================
# 7. 2024
# ======================================

create_market_share_pie(

    2024,

    "Australia Steel Import Market Share — 2024",

    "recent_market_share_2024.png"

)


# ======================================
# 8. 2025
# ======================================

create_market_share_pie(

    2025,

    "Australia Steel Import Market Share — 2025",

    "recent_market_share_2025.png"

)


# ======================================
# 9. 2026 YTD
# ======================================

create_market_share_pie(

    2026,

    "Australia Steel Import Market Share — 2026 YTD",

    "recent_market_share_2026_ytd.png"

)


# ======================================
# 10. SHOW ALL GRAPHS
# ======================================

plt.show()


# ======================================
# COMPLETE
# ======================================

print("\n======================================")
print(" ALL MARKET SHARE PIE CHARTS COMPLETE")
print("======================================")