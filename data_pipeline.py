"""
data_pipeline.py

Reads a raw CSV dataset, cleans it, and loads it into a local SQLite
database (dashboard.db).

Run with: python data_pipeline.py
"""


import sqlite3
import pandas as pd
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

RAW_CSV_PATH = "data/raw_data.csv"
DB_PATH = "dashboard.db"
TABLE_NAME = "records"

COLUMN_MAP = {
    # This dataset (USDA NASS "Corn - Acres Planted") is national-level only
    # (every row is "US TOTAL"), so we use Period (report type: final YEAR
    # value vs. various forecasts) as the category to compare, and Year as
    # the time dimension.
    "Year": "year",
    "Period": "category",
    "Value": "value",
}

# Columns that should be treated as numeric
NUMERIC_COLUMNS = [
    "value",
]

# Column representing time (used for trend charts).
DATE_COLUMN = None  # e.g. "year"

# ---------------------------------------------------------------------------
# Pipeline logic
# ---------------------------------------------------------------------------


def load_raw_data(path: str) -> pd.DataFrame:
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Couldn't find {path}. Download a dataset (see README.md) and "
            f"save it there before running this script."
        )
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df):,} rows and {len(df.columns)} columns from {path}")
    print(f"Columns found: {list(df.columns)}")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Rename columns per COLUMN_MAP
    if COLUMN_MAP:
        df = df.rename(columns=COLUMN_MAP)

    # Drop fully empty rows/columns
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    # Standardize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Coerce numeric columns (strip commas/whitespace)
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(",", "", regex=False).str.strip()
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if NUMERIC_COLUMNS:
        before = len(df)
        df = df.dropna(subset=[c for c in NUMERIC_COLUMNS if c in df.columns])
        print(f"Dropped {before - len(df):,} rows with invalid numeric values")

    # Remove duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    print(f"Dropped {before - len(df):,} duplicate rows")

    print(f"Cleaned dataset: {len(df):,} rows remain")
    return df


def load_to_sqlite(df: pd.DataFrame, db_path: str, table_name: str) -> None:
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"Loaded {len(df):,} rows into '{table_name}' table in {db_path}")


def main():
    df = load_raw_data(RAW_CSV_PATH)
    df = clean_data(df)
    load_to_sqlite(df, DB_PATH, TABLE_NAME)
    print("\nDone. Run `streamlit run app.py` to launch the dashboard.")


if __name__ == "__main__":
    main()
