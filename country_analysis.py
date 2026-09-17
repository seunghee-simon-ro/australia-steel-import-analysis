import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

print("======================================")
print(" AUSTRALIA STEEL IMPORT ANALYSIS")
print("======================================")

# ======================================
# LOAD DATA
# ======================================

df = pd.read_csv("steel_import_by_country.csv")

print("\nData loaded successfully.")
print("Rows:", len(df))


# ======================================
# COUNTRY CODE → COUNTRY NAME
# ======================================

country_map = {
    "NCD": "No Country Details",

    "CHIN": "China",
    "JAP": "Japan",
    "TAIW": "Taiwan",
    "INIA": "India",
    "RKOR": "South Korea",
    "INDO": "Indonesia",

    # Vietnam
    "FGMY": "Vietnam",
    "VIET": "Vietnam",

    "USA": "United States",
    "MLAY": "Malaysia",

    "SWED": "Sweden",
    "SING": "Singapore",
    "ITAL": "Italy",
    "CAN": "Canada",

    "GERM": "Germany",
    "THAI": "Thailand",
    "FINL": "Finland",
    "FRAN": "France",
    "HONG": "Hong Kong",
    "NETH": "Netherlands",
    "BELG": "Belgium",
    "BRAZ": "Brazil",
    "MEXI": "Mexico",
    "SAFR": "South Africa",
    "UK": "United Kingdom",
    "NWAY": "Norway",
    "RUSS": "Russia",
    "SPAN": "Spain",
    "TURK": "Türkiye",
    "PHIL": "Philippines",
    "NEWZ": "New Zealand",
    "IRAN": "Iran",
    "ISRA": "Israel",
    "CHIL": "Chile",
    "ARGN": "Argentina",
    "UAE": "United Arab Emirates",
}


# 국가명 변환
df["COUNTRY_NAME"] = (
    df["COUNTRY_ORIGIN"]
    .map(country_map)
    .fillna(df["COUNTRY_ORIGIN"])
)


# ======================================
# COUNTRY TOTAL
# ======================================

country_total = (
    df.groupby("COUNTRY_NAME")["OBS_VALUE_AUD"]
    .sum()
    .sort_values(ascending=False)
)


# ======================================
# TOP 15
# ======================================

top15 = (
    country_total
    .head(15)
    .sort_values()
)


print("\nTop 15 Source Countries:")

for country, value in top15.sort_values(ascending=False).items():
    print(f"{country:<25} ${value:,.0f}")


# ======================================
# GRAPH
# ======================================

plt.figure(figsize=(14, 9))

ax = top15.plot(
    kind="barh"
)

plt.title(
    "Australia Steel Imports — Top 15 Source Countries",
    fontsize=18,
    pad=15
)

plt.xlabel(
    "Import Value (AUD Billion)",
    fontsize=13
)

plt.ylabel(
    "Country of Origin",
    fontsize=13
)


# ======================================
# X AXIS
# ======================================

ax.xaxis.set_major_formatter(
    FuncFormatter(
        lambda x, pos: f"${x / 1_000_000_000:.1f}B"
    )
)


# ======================================
# VALUE LABELS
# ======================================

for i, value in enumerate(top15):

    ax.text(
        value,
        i,
        f"  ${value / 1_000_000_000:.2f}B",
        va="center",
        fontsize=10
    )


plt.tight_layout()

plt.show()


print("\n======================================")
print(" ANALYSIS COMPLETE")
print("======================================")