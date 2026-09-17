import requests
import pandas as pd
from io import StringIO

print("======================================")
print(" Australia Steel Import Analysis")
print("======================================")
print()

# ABS API
url = (
    "https://data.api.abs.gov.au/rest/data/"
    "ABS,MERCH_IMP,1.0.0/"
    "67.AGUA+ALBA+ANGA+ANGO+ANTC+ANTI+ARGE+ASTA+AUST+BADE+BELA+"
    "BELE+BELG+BHRN+BOHR+BRAZ+BRUN+BULG+BURM+BVIR+CAN+CEAR+CHIN+"
    "CHLE+CHRI+CMBD+COBR+COMB+COST+CROA+CUBA+CYPR+CZEH+DENM+"
    "DMCA+ECUA+EGYP+ESTO+ETMR+FCAM+FGMY+FIJI+FINL+FRAN+FRGU+"
    "FWIN+GERG+GHAN+GIBR+GREE+GUIN+HGRY+HONG+ICEL+INDO+INIA+"
    "IRE+ISRA+ITAL+IVOR+IWAS+JAP+JORD+KAZA+KENY+KUWA+KYRG+LATV+"
    "LEBA+LIBE+LITH+LUX+MACA+MALI+MARS+MASY+MAUS+MEXI+MLAY+"
    "MLDV+MLTA+MNGL+MORO+NAMI+NAUR+NCAL+NCD+NETH+NGRA+NICA+"
    "NIGE+NWAY+NZ+OMAN+PAKI+PERU+PHIL+PLYN+PNG+PNMA+POLA+"
    "PORT+PSIA+QATA+RICO+RKOR+ROUM+RUSS+SAFR+SALV+SAMO+SAUD+"
    "SENE+SERB+SEYC+SING+SLEO+SLOV+SPAI+SRIL+SRNM+SSUD+STCN+"
    "SUDN+SVAK+SWED+SWIT+TAIW+THAI+TOT+TRIN+TUNI+TURK+TURS+"
    "UAEM+UGAN+UK+UKRA+URUG+USA+UZBK+VANU+VENZ+VIET+VIRG+"
    "ZAIR+ZMBA.TOT.M"
)

params = {
    "startPeriod": "2015-01",
    "dimensionAtObservation": "AllDimensions"
}

headers = {
    "Accept": "application/vnd.sdmx.data+csv"
}

print("Downloading ABS steel import data...")
print("Please wait...")
print()

response = requests.get(
    url,
    params=params,
    headers=headers,
    timeout=120
)

print("Status code:", response.status_code)
print("Content-Type:", response.headers.get("content-type"))

response.raise_for_status()

# Convert CSV response into pandas
df = pd.read_csv(StringIO(response.text))

print()
print("Data downloaded successfully!")
print()

# Show columns
print("Columns:")
print(df.columns.tolist())

print()

# Basic information
print("Number of rows:", len(df))

if "COUNTRY_ORIGIN" in df.columns:
    print(
        "Number of countries:",
        df["COUNTRY_ORIGIN"].nunique()
    )

print()

# Convert date
df["TIME_PERIOD"] = pd.to_datetime(
    df["TIME_PERIOD"]
)

# Convert observation value to numeric
df["OBS_VALUE"] = pd.to_numeric(
    df["OBS_VALUE"],
    errors="coerce"
)

# ABS uses UNIT_MULT = 3 for thousands of AUD
# Convert to actual AUD
if "UNIT_MULT" in df.columns:
    df["OBS_VALUE_AUD"] = (
        df["OBS_VALUE"] *
        (10 ** df["UNIT_MULT"])
    )
else:
    df["OBS_VALUE_AUD"] = df["OBS_VALUE"]

# Save raw data
df.to_csv(
    "steel_import_raw.csv",
    index=False
)

print("Raw data saved:")
print("steel_import_raw.csv")
print()

# --------------------------------------
# Monthly total steel imports
# --------------------------------------

monthly = (
    df[df["COUNTRY_ORIGIN"] != "TOT"]
    .groupby("TIME_PERIOD")["OBS_VALUE_AUD"]
    .sum()
    .reset_index()
)

monthly = monthly.sort_values("TIME_PERIOD")

monthly.to_csv(
    "steel_import_monthly.csv",
    index=False
)

print("Monthly data saved:")
print("steel_import_monthly.csv")
print()

# --------------------------------------
# Top importing source countries
# --------------------------------------

country_total = (
    df[df["COUNTRY_ORIGIN"] != "TOT"]
    .groupby("COUNTRY_ORIGIN")["OBS_VALUE_AUD"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

country_total.to_csv(
    "steel_import_by_country.csv",
    index=False
)

print("Country data saved:")
print("steel_import_by_country.csv")
print()

print("Top 10 source countries:")
print(country_total.head(10))

print()
print("======================================")
print(" DONE")
print("======================================")