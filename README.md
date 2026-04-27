# 🌍 Global Natural Disasters Dashboard

An interactive data science dashboard analysing global natural disaster trends from 2000 to 2024, built with **Streamlit** and **Plotly**.

Developed as part of the **5DATA004C Data Science Project Lifecycle** module at the University of Westminster.

---

## 👤 Student Information

| Name | Yogaraja Bawadharani |
| UoW ID | w2149494 |
| IIT ID | 20233004 |
| Module | 5DATA004C · University of Westminster |

---

## 📊 About the Dashboard

This dashboard provides an in-depth analysis of global natural disaster data sourced from the **EM-DAT International Disaster Database** (CRED), accessed via the **Humanitarian Data Exchange (HDX)**.

It was designed for high-level decision-makers, finance professionals, and technology experts attending a global sustainability conference — providing actionable insights into the frequency, scale, and economic toll of natural disasters worldwide.

### Research Questions

| RQ | Question |
|---|---|
| RQ1 | Which disaster types cause the most deaths globally? |
| RQ2 | Has the frequency of natural disasters increased over time? |
| RQ3 | Which countries are most economically and humanitarianly impacted? |
| RQ4 | Which disasters affect the largest number of people? |

---

## 🗂️ Dashboard Pages

| Page | Description |
|---|---|
| 🏠 Overview | Summary statistics, KPI strip, and snapshot charts |
| 📋 Executive Summary | Evidence-based answers to all four research questions |
| 🗺️ Geographic Impact | Choropleth world map and disaster type breakdown |
| 📈 Trends Over Time | Frequency and economic damage trends by year |
| 🔍 Distribution Analysis | Donut chart, bubble scatter, and subgroup breakdown |
| 🏆 Country Rankings | Top 10 and least-affected country comparisons |
| 📋 Data Table | Filtered raw data with CSV export |

---

## 🛠️ Tech Stack

- **Python 3.x**
- **Streamlit** — web application framework
- **Plotly** — interactive visualisations
- **Pandas** — data manipulation and filtering

---

## 📁 Project Structure

```
natural-disasters-dashboard/

app.py                        # Main Streamlit application
emdat_cleaned.csv             # Cleaned EM-DAT dataset
requirements.txt              # Python dependencies
.gitignore                    # Git ignore rules
README.md                     # This file
```

---

## 🚀 How to Run Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/natural-disasters-dashboard.git
   cd natural-disasters-dashboard
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

4. Open your browser at `http://localhost:8501`

---

## 🌐 Live Deployment

This dashboard is deployed on **Streamlit Community Cloud**.

> 🔗 [View Live Dashboard](https://natural-disasters-dashboard-uhtzdmygxz23xepzelk4ex.streamlit.app/)


---

## 📦 Dataset

- **Source:** EM-DAT — The International Disaster Database
- **Provider:** Centre for Research on the Epidemiology of Disasters (CRED)
- **Accessed via:** Humanitarian Data Exchange (HDX)
- **Coverage:** 2000–2024, 190+ countries

---

## ✨ Key Features

- Fully interactive sidebar filters (year range, disaster type, subgroup, country)
- Dynamic KPI strip that updates with every filter change
- Choropleth world map with switchable metrics
- Inflation-adjusted economic damage analysis
- Bubble scatter chart comparing deaths vs. people affected
- CSV export of filtered data
- Clean light theme with formal typography (Merriweather + Inter)
- Permanent sidebar — no collapse/hide behaviour

---

*5DATA004C Data Science Project Lifecycle · University of Westminster*
