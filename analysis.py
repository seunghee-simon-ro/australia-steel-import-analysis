import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


# ======================================
# AUSTRALIA STEEL IMPORT ANALYSIS
# ======================================

print("======================================")
print(" AUSTRALIA STEEL IMPORT ANALYSIS")
print("======================================")


# ======================================
# 1. LOAD DATA
# ======================================

print("\nLoading data...")

df = pd.read_csv("steel_import_raw.csv")

# Convert date
df["TIME_PERIOD"] = pd.to_datetime(df["TIME_PERIOD"])

# Convert OBS_VALUE to AUD
# UNIT_MULT = 3 → thousand AUD
df["OBS_VALUE_AUD"] = df["OBS_VALUE"] * 1000

print("Data loaded successfully.")


# ======================================
# 2. DATA VALIDATION
# ======================================

print("\n======================================")
print(" DATA VALIDATION")
print("======================================")

print("\n1. Dataset size")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\n2. Columns")
print(df.columns.tolist())

print("\n3. Countries")
print(
    "Number of countries:",
    df["COUNTRY_ORIGIN"].nunique()
)

print("\n4. Date range")
print(
    "From:",
    df["TIME_PERIOD"].min()
)

print(
    "To:",
    df["TIME_PERIOD"].max()
)

print("\n5. Units")
print(
    "UNIT_MEASURE:",
    df["UNIT_MEASURE"].unique()
)

print(
    "UNIT_MULT:",
    df["UNIT_MULT"].unique()
)

print("\n6. Commodity")
print(
    df["COMMODITY_SITC"].unique()
)

print("\n7. Destination")
print(
    df["STATE_DEST"].unique()
)

print("\n8. Frequency")
print(
    df["FREQ"].unique()
)

print("\n9. Missing values")
print(
    df.isnull().sum()
)

print("\n10. Total OBS_VALUE")
print(
    f"{df['OBS_VALUE'].sum():,.0f}"
)

print("\n11. First 10 rows")

print(
    df.head(10).to_string(index=False)
)

print("\n======================================")
print(" VALIDATION COMPLETE")
print("======================================")


# ======================================
# 3. MONTHLY ANALYSIS
# ======================================

monthly = (
    df.groupby("TIME_PERIOD")["OBS_VALUE_AUD"]
    .sum()
    .reset_index()
)

monthly["IMPORT_VALUE_BILLION_AUD"] = (
    monthly["OBS_VALUE_AUD"]
    / 1_000_000_000
)

print("\n======================================")
print(" MONTHLY STEEL IMPORT ANALYSIS")
print("======================================")

print(
    "\nNumber of months:",
    len(monthly)
)

print("\nDate range:")

print(
    monthly["TIME_PERIOD"].min(),
    "to",
    monthly["TIME_PERIOD"].max()
)

print("\nMonthly import values:")

print(
    monthly[
        [
            "TIME_PERIOD",
            "IMPORT_VALUE_BILLION_AUD"
        ]
    ].to_string(index=False)
)


# Save monthly data

monthly.to_csv(
    "steel_import_monthly_clean.csv",
    index=False
)


# ======================================
# 4. ANNUAL ANALYSIS
# ======================================

df["YEAR"] = df["TIME_PERIOD"].dt.year

annual = (
    df.groupby("YEAR")["OBS_VALUE_AUD"]
    .sum()
    .reset_index()
)

annual["IMPORT_VALUE_BILLION_AUD"] = (
    annual["OBS_VALUE_AUD"]
    / 1_000_000_000
)

print("\n======================================")
print(" ANNUAL STEEL IMPORT ANALYSIS")
print("======================================")

print("\nAnnual import values:")

print(
    annual[
        [
            "YEAR",
            "IMPORT_VALUE_BILLION_AUD"
        ]
    ].to_string(index=False)
)


# Save annual data

annual.to_csv(
    "steel_import_annual_clean.csv",
    index=False
)


# ======================================
# 5. COUNTRY ANALYSIS
# ======================================

print("\n======================================")
print(" COUNTRY ANALYSIS")
print("======================================")


country_data = (
    df.groupby("COUNTRY_ORIGIN")["OBS_VALUE_AUD"]
    .sum()
    .reset_index()
)


# ======================================
# REMOVE TOTAL
# ======================================

country_data = country_data[
    country_data["COUNTRY_ORIGIN"] != "TOT"
]


# Sort by import value

country_data = country_data.sort_values(
    "OBS_VALUE_AUD",
    ascending=False
)


# ======================================
# 6. COUNTRY CODE → COUNTRY NAME
# ======================================

country_names = {

    # Special
    "NCD": "No Country Details",

    # Major countries
    "CHIN": "China",
    "JAP": "Japan",
    "TAIW": "Taiwan",
    "INIA": "India",
    "RKOR": "South Korea",
    "INDO": "Indonesia",

    # Germany
    "FGMY": "Germany",

    "USA": "United States",
    "MLAY": "Malaysia",

    # Europe / Asia
    "SWED": "Sweden",
    "VIET": "Vietnam",
    "ITAL": "Italy",
    "SING": "Singapore",
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
    "JPN": "Japan",
    "KOR": "South Korea",
    "HONG": "Hong Kong",

    "TURK": "Turkey",
    "SWIT": "Switzerland",
    "AUSTR": "Austria",
    "POLA": "Poland",
    "CZEH": "Czech Republic",
    "RUMA": "Romania",

    "PHIL": "Philippines",
    "PAKI": "Pakistan",
    "BANGL": "Bangladesh",

    "SAUD": "Saudi Arabia",
    "UAE": "United Arab Emirates",

    "IRAN": "Iran",
}


# Create country name

country_data["COUNTRY_NAME"] = (
    country_data["COUNTRY_ORIGIN"]
    .map(country_names)
    .fillna(
        country_data["COUNTRY_ORIGIN"]
    )
)


# Convert to billion AUD

country_data["IMPORT_VALUE_BILLION_AUD"] = (
    country_data["OBS_VALUE_AUD"]
    / 1_000_000_000
)


# ======================================
# 7. COUNTRY OUTPUT
# ======================================

print("\nTop 15 source countries:")

print(
    country_data[
        [
            "COUNTRY_ORIGIN",
            "COUNTRY_NAME",
            "IMPORT_VALUE_BILLION_AUD"
        ]
    ]
    .head(15)
    .to_string(index=False)
)


# Save country data

country_data.to_csv(
    "steel_import_by_country_clean.csv",
    index=False
)


# ======================================
# 8. TOP 15 COUNTRIES
# ======================================

top15 = (
    country_data
    .head(15)
    .sort_values(
        "IMPORT_VALUE_BILLION_AUD",
        ascending=True
    )
)


# ======================================
# 9. GRAPH 1
# MONTHLY TREND
# ======================================

plt.figure(
    figsize=(14, 7)
)

plt.plot(
    monthly["TIME_PERIOD"],
    monthly["IMPORT_VALUE_BILLION_AUD"]
)

plt.title(
    "Australia Steel Imports — Monthly Trend",
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

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()


# ======================================
# 10. GRAPH 2
# ANNUAL TREND
# ======================================

plt.figure(
    figsize=(14, 7)
)

plt.bar(
    annual["YEAR"].astype(str),
    annual["IMPORT_VALUE_BILLION_AUD"]
)

plt.title(
    "Australia Steel Imports — Annual Trend",
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
    rotation=45
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()


# ======================================
# 11. GRAPH 3
# TOP 15 SOURCE COUNTRIES
# ======================================

plt.figure(
    figsize=(14, 9)
)

plt.barh(
    top15["COUNTRY_NAME"],
    top15["IMPORT_VALUE_BILLION_AUD"]
)

plt.title(
    "Australia Steel Imports — Top 15 Source Countries",
    fontsize=18
)

plt.xlabel(
    "Import Value (AUD Billion)",
    fontsize=12
)

plt.ylabel(
    "Country of Origin",
    fontsize=12
)


# Format X axis

def format_billions(
    x,
    pos
):
    return f"${x:.1f}B"


plt.gca().xaxis.set_major_formatter(
    FuncFormatter(format_billions)
)


plt.grid(
    axis="x",
    alpha=0.3
)

plt.tight_layout()


# ======================================
# 12. SHOW GRAPHS
# ======================================

plt.show()


# ======================================
# COMPLETE
# ======================================

print("\n======================================")
print(" ANALYSIS COMPLETE")
print("======================================")

print("\nSaved files:")

print(
    "steel_import_monthly_clean.csv"
)

print(
    "steel_import_annual_clean.csv"
)

print(
    "steel_import_by_country_clean.csv"
)