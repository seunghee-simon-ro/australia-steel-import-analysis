# 🇦🇺 Australia Steel Import Market Analysis

Analysis of Australia's steel import market using monthly Australian Bureau of Statistics (ABS) data.

This project examines Australia's steel import trends, major source countries, market shares, and South Korea's position in the Australian steel import market.

---

## 📌 Project Overview

This project analyses Australia's steel imports from **January 2015 to July 2026**, with a focus on:

- Overall Australian steel import trends
- Annual and monthly import values
- Major source countries
- Recent country-level import trends
- Market share by source country
- South Korea's long-term market position
- Recent changes in the competitive landscape

The analysis provides a data-driven view of Australia's steel import market and changes in major supply sources over time.

---

## 📊 Data

**Source:** Australian Bureau of Statistics (ABS)

**Dataset:** Merchandise Imports

**Commodity:** SITC 67 — Iron and Steel

**Period:** January 2015 – July 2026

**Frequency:** Monthly

**Destination:** Australia (Total)

**Measure:** Import Value (AUD)

The data was retrieved from the ABS SDMX API and processed using Python.

---

## 📈 Australian Steel Import Trend

### Monthly Trend

![Monthly Steel Import Trend](australia_steel_import_trend.png)

### Annual Trend

![Annual Steel Import Trend](australia_steel_import_annual.png)

The annual data shows considerable fluctuations in Australia's steel import value, with import levels increasing substantially during the early 2020s compared with the mid-to-late 2010s.

---

## 🌏 Source Country Analysis

The project analyses Australia's steel imports by country of origin.

### Recent Country Import Trends

![Recent Country Import Trends](recent_country_import_trends.png)

The analysis identifies major steel supply sources and tracks changes in their import values over time.

Countries with unidentified origin information are reported separately as **"No Country Details"** rather than being treated as a specific country.

---

## 🥧 Market Share Analysis

Recent market share was analysed using import values by country.

### 2024

![2024 Market Share](recent_market_share_2024.png)

### 2025

![2025 Market Share](recent_market_share_2025.png)

### 2026 YTD

![2026 YTD Market Share](recent_market_share_2026_ytd.png)

**Note:** 2026 represents **Year-to-Date (YTD) data through July 2026**, rather than a full-year figure.

---

## 🇰🇷 South Korea

South Korea is analysed separately to examine its long-term position in Australia's steel import market.

### South Korea Market Share Trend

![South Korea Market Share Trend](south_korea_market_share_trend.png)

The analysis tracks changes in South Korea's import value and market share over the long term and compares its position with other major source countries.

---

## 🌎 Major Countries

The project also compares market-share movements among major steel-exporting countries.

![Major Countries Market Share Trend](major_countries_market_share_trend.png)

This provides a longer-term view of how Australia's supplier composition has changed.

---

## 📁 Analysis Outputs

The project generates several CSV datasets for further analysis:

| File | Description |
|---|---|
| `steel_import_raw.csv` | Raw ABS import data |
| `steel_import_monthly.csv` | Monthly import data |
| `steel_import_monthly_clean.csv` | Cleaned monthly dataset |
| `steel_import_by_country.csv` | Import data by source country |
| `steel_import_by_country_clean.csv` | Cleaned country-level data |
| `steel_import_annual_clean.csv` | Annual import values |
| `long_term_import_value.csv` | Long-term country import values |
| `long_term_market_share.csv` | Long-term market share |
| `long_term_country_analysis.csv` | Long-term country analysis |
| `2025_country_ranking.csv` | 2025 country ranking |
| `2026_country_ytd.csv` | 2026 YTD country ranking |
| `recent_market_share_comparison.csv` | Recent market-share comparison |
| `south_korea_long_term_trend.csv` | South Korea long-term trend |

---

## 💻 Python Analysis

The analysis was conducted using Python and includes:

- `get_data.py` — Retrieves data from the ABS API
- `analysis.py` — Data validation and monthly/annual analysis
- `country_analysis.py` — Country-level analysis
- `country_comparison.py` — Country comparisons
- `long_term_country_analysis.py` — Long-term country analysis
- `market_share.py` — Market-share analysis
- `market_share_pie.py` — Market-share visualisation
- `recent_market_analysis.py` — Recent market analysis
- `recent_country_trends.py` — Recent country trends
- `recent_market_share_pies.py` — Recent market-share pie charts

---

## 🛠️ Tools & Technologies

- **Python**
- **Pandas**
- **Matplotlib**
- **ABS SDMX API**
- **CSV data processing**
- **Data visualisation**
- **Git / GitHub**

---

## 🎯 Project Purpose

The purpose of this project is to use publicly available trade data to understand the structure and evolution of Australia's steel import market.

The analysis can be used to examine:

- Changes in Australia's overall steel import demand
- Shifts in major supply countries
- Changes in supplier market share
- South Korea's position in the market
- Changes in Australia's steel supply landscape

---

## 📌 Data Limitations

The latest available observation in this project is **July 2026**. Therefore, 2026 annual figures and market shares represent **YTD data** and should not be interpreted as full-year results.

Some ABS records contain an unspecified country of origin. These observations are labelled **"No Country Details"** and are kept separate from identified source countries.

---

## 📚 Data Source

Australian Bureau of Statistics — Merchandise Imports

**Commodity:** SITC 67 — Iron and Steel