"""
queries.py

SQL queries run against dashboard.db.
"""

import sqlite3
import pandas as pd

DB_PATH = "dashboard.db"
TABLE_NAME = "records"


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_all_records() -> pd.DataFrame:
    query = f"SELECT * FROM {TABLE_NAME}"
    with get_connection() as conn:
        return pd.read_sql_query(query, conn)


def get_distinct_values(column: str) -> list:
    """Get unique values for a filter dropdown, e.g. distinct regions."""
    query = f"SELECT DISTINCT {column} FROM {TABLE_NAME} ORDER BY {column}"
    with get_connection() as conn:
        return pd.read_sql_query(query, conn)[column].tolist()


def get_filtered_records(filters: dict) -> pd.DataFrame:
    """
    filters: dict of {column_name: value} to filter on.
    Example: {"region": "Maryland"}
    """
    query = f"SELECT * FROM {TABLE_NAME}"
    params = []
    if filters:
        conditions = []
        for col, val in filters.items():
            conditions.append(f"{col} = ?")
            params.append(val)
        query += " WHERE " + " AND ".join(conditions)

    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)


def get_trend_over_time(date_column: str, value_column: str, group_by: str = None) -> pd.DataFrame:
    """
    Aggregate a numeric value column over time, optionally grouped by
    another category (e.g. region).
    """
    if group_by:
        query = f"""
            SELECT {date_column}, {group_by}, AVG({value_column}) as avg_value
            FROM {TABLE_NAME}
            GROUP BY {date_column}, {group_by}
            ORDER BY {date_column}
        """
    else:
        query = f"""
            SELECT {date_column}, AVG({value_column}) as avg_value
            FROM {TABLE_NAME}
            GROUP BY {date_column}
            ORDER BY {date_column}
        """
    with get_connection() as conn:
        return pd.read_sql_query(query, conn)


def get_top_n(column_to_rank: str, value_column: str, n: int = 10, ascending: bool = False) -> pd.DataFrame:
    """Get the top (or bottom) N rows ranked by a numeric column."""
    order = "ASC" if ascending else "DESC"
    query = f"""
        SELECT {column_to_rank}, {value_column}
        FROM {TABLE_NAME}
        ORDER BY {value_column} {order}
        LIMIT {n}
    """
    with get_connection() as conn:
        return pd.read_sql_query(query, conn)


def get_summary_stats(value_column: str) -> dict:
    query = f"""
        SELECT
            COUNT(*) as count,
            AVG({value_column}) as mean,
            MIN({value_column}) as min,
            MAX({value_column}) as max
        FROM {TABLE_NAME}
    """
    with get_connection() as conn:
        result = pd.read_sql_query(query, conn)
    return result.iloc[0].to_dict()
