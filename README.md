# Public Data Insights Dashboard

A Python + SQL + Streamlit dashboard project — built to
demonstrate data analysis, SQL, and UI/UX skills.

**Live demo:** [public-data-insights-dashboard.streamlit.app](https://public-data-insights-dashboard.streamlit.app/)

Currently loaded with USDA NASS "Corn - Acres Planted" data (US national totals, 1926–2026), comparing final year estimates against in-season forecasts (March/June/August/September/October acreage reports).

## Project structure

```
dashboard_project/
├── data/
│   └── raw_data.csv          <- raw dataset here
├── data_pipeline.py          <- cleans raw data, loads it into SQLite
├── queries.py                <- SQL queries against the database
├── app.py                    <- streamlit dashboard
├── dashboard.db              <- created automatically when you run the pipeline
└── README.md
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Build the database

```bash
python data_pipeline.py
```

This reads `data/raw_data.csv`, cleans it, and writes it into `dashboard.db`.

## Run the dashboard

```bash
streamlit run app.py
```

This opens an interactive dashboard in your browser with:
- A filterable data table
- A trend chart over time
- A comparison view across categories
- A written insights panel (you fill in the takeaways once you see the data)

