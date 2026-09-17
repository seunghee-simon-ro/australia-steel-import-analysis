import pandas as pd
import matplotlib.pyplot as plt


# ======================================
# AUSTRALIA STEEL IMPORT
# 2025 MARKET SHARE PIE CHART
# ======================================

print("======================================")
print(" 2025 AUSTRALIA STEEL IMPORT")
print(" MARKET SHARE PIE CHART")
print("======================================")


# ======================================
# 1. LOAD DATA
# ======================================

df = pd.read_csv("steel_import_raw.csv")

df["TIME_PERIOD"] = pd.to_datetime(
    df["TIME_PERIOD"]
)

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
# 3. COUNTRY NAMES
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
# 4. SELECT 2025
# ======================================

df_2025 = df[
    df["TIME_PERIOD"].dt.year == 2025
]


# ======================================
# 5. COUNTRY TOTAL
# ======================================

country = (
    df_2025
    .groupby("COUNTRY_NAME")["OBS_VALUE_AUD"]
    .sum()
    .sort_values(
        ascending=False
    )
)


# ======================================
# 6. TOP 5 + OTHERS
# ======================================

top5 = country.head(5)

others = country.iloc[5:].sum()


pie_data = top5.copy()

pie_data["Others"] = others


# Convert to billion AUD

pie_billion = (
    pie_data / 1_000_000_000
)


# ======================================
# 7. PRINT RESULTS
# ======================================

print("\n======================================")
print(" 2025 MARKET SHARE")
print("======================================")

total = pie_data.sum()

for country_name, value in pie_data.items():

    share = (
        value / total * 100
    )

    print(
        f"{country_name:25s}"
        f" {value / 1_000_000_000:8.2f} "
        f"billion AUD"
        f" ({share:5.1f}%)"
    )


# ======================================
# 8. PIE CHART
# ======================================

plt.figure(
    figsize=(10, 10)
)


plt.pie(
    pie_data,
    labels=pie_data.index,
    autopct="%1.1f%%",
    startangle=90
)


plt.title(
    "Australia Steel Import Market Share — 2025",
    fontsize=18
)


plt.tight_layout()


# ======================================
# 9. SAVE DATA
# ======================================

pie_output = pd.DataFrame({
    "COUNTRY": pie_data.index,
    "IMPORT_VALUE_BILLION_AUD": pie_billion.values,
    "MARKET_SHARE_%":
        pie_data.values
        / pie_data.sum()
        * 100
})


pie_output.to_csv(
    "steel_import_2025_pie.csv",
    index=False
)


print("\n======================================")
print(" COMPLETE")
print("======================================")

print(
    "\nSaved:"
)

print(
    "steel_import_2025_pie.csv"
)


# ======================================
# 10. SHOW
# ======================================

plt.show()