import pandas as pd
import matplotlib.pyplot as plt


# ======================================
# KOREA vs CHINA vs JAPAN
# AUSTRALIA STEEL IMPORT ANALYSIS
# ======================================

print("======================================")
print(" KOREA vs CHINA vs JAPAN")
print(" AUSTRALIA STEEL IMPORTS")
print("======================================")


# ======================================
# 1. LOAD RAW DATA
# ======================================

df = pd.read_csv("steel_import_raw.csv")

# Convert date
df["TIME_PERIOD"] = pd.to_datetime(df["TIME_PERIOD"])

# Convert to AUD
df["OBS_VALUE_AUD"] = df["OBS_VALUE"] * 1000

# Remove total row
df = df[
    df["COUNTRY_ORIGIN"] != "TOT"
]


# ======================================
# 2. SELECT COUNTRIES
# ======================================

countries = {
    "CHIN": "China",
    "RKOR": "South Korea",
    "JAP": "Japan"
}

comparison = df[
    df["COUNTRY_ORIGIN"].isin(countries.keys())
].copy()

comparison["COUNTRY_NAME"] = (
    comparison["COUNTRY_ORIGIN"]
    .map(countries)
)


# ======================================
# 3. ANNUAL DATA
# ======================================

comparison["YEAR"] = (
    comparison["TIME_PERIOD"].dt.year
)

annual = (
    comparison
    .groupby(
        ["YEAR", "COUNTRY_NAME"]
    )["OBS_VALUE_AUD"]
    .sum()
    .reset_index()
)


# Convert to billion AUD

annual["IMPORT_VALUE_BILLION_AUD"] = (
    annual["OBS_VALUE_AUD"]
    / 1_000_000_000
)


# ======================================
# 4. PRINT ANNUAL RESULTS
# ======================================

print("\n======================================")
print(" ANNUAL IMPORT VALUE")
print("======================================")

print(
    annual[
        [
            "YEAR",
            "COUNTRY_NAME",
            "IMPORT_VALUE_BILLION_AUD"
        ]
    ].to_string(index=False)
)


# ======================================
# 5. PIVOT TABLE
# ======================================

annual_pivot = annual.pivot(
    index="YEAR",
    columns="COUNTRY_NAME",
    values="IMPORT_VALUE_BILLION_AUD"
).fillna(0)


print("\n======================================")
print(" KOREA vs CHINA vs JAPAN")
print("======================================")

print(
    annual_pivot.to_string()
)


# ======================================
# 6. YEAR-ON-YEAR GROWTH
# ======================================

growth = annual_pivot.pct_change() * 100

print("\n======================================")
print(" YEAR-ON-YEAR GROWTH (%)")
print("======================================")

print(
    growth.round(1).to_string()
)


# ======================================
# 7. GRAPH — ANNUAL TREND
# ======================================

plt.figure(
    figsize=(14, 8)
)

for country in [
    "China",
    "South Korea",
    "Japan"
]:

    if country in annual_pivot.columns:

        plt.plot(
            annual_pivot.index,
            annual_pivot[country],
            marker="o",
            label=country
        )


plt.title(
    "Australia Steel Imports — China vs South Korea vs Japan",
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

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()


# ======================================
# 8. 2026 YTD
# ======================================

ytd_2026 = comparison[
    comparison["TIME_PERIOD"].dt.year == 2026
].copy()


ytd_2026_total = (
    ytd_2026
    .groupby("COUNTRY_NAME")["OBS_VALUE_AUD"]
    .sum()
    / 1_000_000_000
)


print("\n======================================")
print(" 2026 YTD")
print("======================================")

print(
    ytd_2026_total
    .sort_values(
        ascending=False
    )
    .round(3)
    .to_string()
)


# ======================================
# 9. SAVE RESULTS
# ======================================

annual.to_csv(
    "korea_china_japan_annual.csv",
    index=False
)

annual_pivot.to_csv(
    "korea_china_japan_comparison.csv"
)

growth.to_csv(
    "korea_china_japan_growth.csv"
)


print("\n======================================")
print(" ANALYSIS COMPLETE")
print("======================================")

print("\nSaved:")
print("korea_china_japan_annual.csv")
print("korea_china_japan_comparison.csv")
print("korea_china_japan_growth.csv")


# ======================================
# SHOW GRAPH
# ======================================

plt.show()