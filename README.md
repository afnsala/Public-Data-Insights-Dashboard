# Public Data Insights Dashboard

A Python + SQL + Streamlit dashboard project — built to
demonstrate data analysis, SQL, and UI/UX skills

## Project structure

```
dashboard_project/
├── data/
│   └── raw_data.csv          <- raw dataset here
├── data_pipeline.py           <- cleans raw data, loads it into SQLite
├── queries.py                 <- SQL queries against the database
├── app.py                     <- streamlit dashboard
├── dashboard.db                <- created automatically when you run the pipeline
└── README.md
```

## Install dependencies

```bash
pip install pandas streamlit plotly
```

## Build the database

```bash
python data_pipeline.py
```

This reads `data/raw_data.csv`, cleans it, and writes it into `dashboard.db`

## Run the dashboard

```bash
streamlit run app.py
```

This opens an interactive dashboard in your browser with:
- A filterable data table
- A trend chart over time
- A comparison view across categories
- A written insights panel (you fill in the takeaways once you see the data)

## Deploy it 

Push, then deploy at https://share.streamlit.io 