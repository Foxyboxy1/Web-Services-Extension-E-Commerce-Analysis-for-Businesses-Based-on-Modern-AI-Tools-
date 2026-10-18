"""Data layer for the Superstore Analytics dashboard.

This module owns every calculation performed on the Superstore dataset:
loading, filtering, KPI computation and chart aggregations. It deliberately
contains no presentation or translation logic so it can be reused and tested
independently of Flask.
"""

from __future__ import annotations

import os
from datetime import date, timedelta
from functools import lru_cache

import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "Sample-Superstore.csv")

DATE_FMT = "%Y-%m-%d"
NUMERIC_COLUMNS = ("Sales", "Profit", "Quantity", "Discount")

# Columns that make up the "filter options" exposed to the UI.
FILTER_COLUMNS = {
    "region": "Region",
    "category": "Category",
    "segment": "Segment",
}


@lru_cache(maxsize=1)
def load_data() -> pd.DataFrame:
    """Load and normalise the Superstore dataset (cached for the process)."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")

    # The source file contains a stray BOM inside the header row.
    df.columns = [str(col).strip().lstrip("\ufeff") for col in df.columns]

    for column in ("Order Date", "Ship Date"):
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    for column in NUMERIC_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=["Sales", "Profit", "Order Date"])
    return df.reset_index(drop=True)


def date_bounds(df: pd.DataFrame) -> dict:
    """Smallest and largest order dates present in the dataset."""
    if df.empty:
        today = date.today()
        return {"min": today, "max": today}
    return {
        "min": df["Order Date"].min().date(),
        "max": df["Order Date"].max().date(),
    }


def filter_options(df: pd.DataFrame) -> dict:
    """Distinct values used to populate the filter dropdowns."""
    options: dict[str, list[str]] = {}
    for key, column in FILTER_COLUMNS.items():
        if column in df.columns:
            values = df[column].dropna().unique().tolist()
            options[key] = sorted(values)
        else:
            options[key] = []
    return options


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return pd.to_datetime(value, format=DATE_FMT).date()
    except (ValueError, TypeError):
        return None


def normalise_filters(filters: dict | None) -> dict:
    """Coerce raw request values into a clean, validated filter dictionary."""
    filters = filters or {}
    normalised = {
        "start_date": _parse_date(filters.get("start_date")),
        "end_date": _parse_date(filters.get("end_date")),
        "region": (filters.get("region") or "").strip(),
        "category": (filters.get("category") or "").strip(),
        "segment": (filters.get("segment") or "").strip(),
        "search": (filters.get("search") or "").strip(),
    }
    # Guard against an inverted range coming from the UI.
    if (
        normalised["start_date"]
        and normalised["end_date"]
        and normalised["start_date"] > normalised["end_date"]
    ):
        normalised["start_date"], normalised["end_date"] = (
            normalised["end_date"],
            normalised["start_date"],
        )
    return normalised


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Return the subset of the dataset matching the active filters."""
    result = df

    if filters.get("start_date") is not None:
        result = result[result["Order Date"].dt.date >= filters["start_date"]]
    if filters.get("end_date") is not None:
        result = result[result["Order Date"].dt.date <= filters["end_date"]]
    if filters.get("region"):
        result = result[result["Region"] == filters["region"]]
    if filters.get("category"):
        result = result[result["Category"] == filters["category"]]
    if filters.get("segment"):
        result = result[result["Segment"] == filters["segment"]]

    search = filters.get("search")
    if search:
        needle = search.casefold()
        haystack = (
            result["Product Name"].fillna("").str.casefold()
            + " "
            + result["Customer Name"].fillna("").str.casefold()
            + " "
            + result["City"].fillna("").str.casefold()
        )
        result = result[haystack.str.contains(needle, regex=False, na=False)]

    return result


def compute_kpis(df: pd.DataFrame) -> dict:
    """Core KPIs derived strictly from the supplied rows."""
    total_sales = float(df["Sales"].sum()) if not df.empty else 0.0
    total_profit = float(df["Profit"].sum()) if not df.empty else 0.0
    total_orders = int(df["Order ID"].nunique()) if not df.empty else 0
    total_quantity = int(df["Quantity"].sum()) if not df.empty else 0
    total_customers = int(df["Customer ID"].nunique()) if not df.empty else 0

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "total_orders": total_orders,
        "total_quantity": total_quantity,
        "total_customers": total_customers,
        "profit_margin": (total_profit / total_sales * 100) if total_sales else 0.0,
        "avg_order_value": (total_sales / total_orders) if total_orders else 0.0,
        "has_data": not df.empty,
    }


def _previous_period(filters: dict) -> dict | None:
    """Build a filter set describing the period immediately before the range."""
    start, end = filters.get("start_date"), filters.get("end_date")
    if start is None or end is None:
        return None

    span = end - start
    previous_end = start - timedelta(days=1)
    previous_start = previous_end - span

    previous = dict(filters)
    previous["start_date"] = previous_start
    previous["end_date"] = previous_end
    return previous


def _delta(current: dict, previous: dict) -> dict:
    """Percentage change per KPI, or percentage points for margin."""
    deltas: dict[str, float | None] = {
        "total_sales": _pct_change(current["total_sales"], previous["total_sales"]),
        "total_profit": _pct_change(current["total_profit"], previous["total_profit"]),
        "total_orders": _pct_change(current["total_orders"], previous["total_orders"]),
        "avg_order_value": _pct_change(
            current["avg_order_value"], previous["avg_order_value"]
        ),
        "total_quantity": _pct_change(
            current["total_quantity"], previous["total_quantity"]
        ),
        # Margin movement is expressed in percentage points, not percent.
        "profit_margin": (
            round(current["profit_margin"] - previous["profit_margin"], 2)
            if previous["total_sales"]
            else None
        ),
    }
    deltas["profit_margin_unit"] = "pp"
    return deltas


def _pct_change(current: float, previous: float) -> float | None:
    if not previous:
        return None
    return round((current - previous) / abs(previous) * 100, 2)


def _group_totals(df: pd.DataFrame, column: str) -> list[dict]:
    if df.empty or column not in df.columns:
        return []

    grouped = (
        df.groupby(column, dropna=True)
        .agg(sales=("Sales", "sum"), profit=("Profit", "sum"), orders=("Order ID", "nunique"))
        .reset_index()
        .sort_values("sales", ascending=False)
    )

    total_sales = float(grouped["sales"].sum()) or 1.0
    return [
        {
            "key": str(row[column]),
            "sales": float(row["sales"]),
            "profit": float(row["profit"]),
            "orders": int(row["orders"]),
            "share": float(row["sales"]) / total_sales * 100,
        }
        for _, row in grouped.iterrows()
    ]


def _monthly_trend(df: pd.DataFrame) -> list[dict]:
    if df.empty:
        return []

    working = df.copy()
    working["_month"] = working["Order Date"].dt.strftime("%Y-%m")
    grouped = (
        working.groupby("_month")
        .agg(sales=("Sales", "sum"), profit=("Profit", "sum"))
        .reset_index()
        .sort_values("_month")
    )
    return [
        {
            "month": str(row["_month"]),
            "sales": float(row["sales"]),
            "profit": float(row["profit"]),
        }
        for _, row in grouped.iterrows()
    ]


def _top_products(df: pd.DataFrame, limit: int = 8) -> list[dict]:
    if df.empty:
        return []

    grouped = (
        df.groupby(["Product Name", "Category", "Sub-Category"], dropna=True)
        .agg(
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
            quantity=("Quantity", "sum"),
        )
        .reset_index()
        .sort_values("sales", ascending=False)
        .head(limit)
    )

    products = []
    for _, row in grouped.iterrows():
        sales = float(row["sales"])
        profit = float(row["profit"])
        products.append(
            {
                "name": str(row["Product Name"]),
                "category": str(row["Category"]),
                "sub_category": str(row["Sub-Category"]),
                "sales": sales,
                "profit": profit,
                "quantity": int(row["quantity"]),
                "margin": (profit / sales * 100) if sales else 0.0,
            }
        )
    return products


def build_dashboard(df: pd.DataFrame, filters: dict) -> dict:
    """Aggregate everything the dashboard templates need, in one pass."""
    filtered = apply_filters(df, filters)
    kpis = compute_kpis(filtered)

    previous_filters = _previous_period(filters)
    if previous_filters is not None:
        previous_kpis = compute_kpis(apply_filters(df, previous_filters))
        kpis["deltas"] = _delta(kpis, previous_kpis) if previous_kpis["has_data"] else None
        kpis["comparison_available"] = bool(previous_kpis["has_data"])
    else:
        kpis["deltas"] = None
        kpis["comparison_available"] = False

    return {
        "kpis": kpis,
        "trend": _monthly_trend(filtered),
        "categories": _group_totals(filtered, "Category"),
        "regions": _group_totals(filtered, "Region"),
        "segments": _group_totals(filtered, "Segment"),
        "sub_categories": _group_totals(filtered, "Sub-Category"),
        "top_products": _top_products(filtered),
        "row_count": int(len(filtered)),
    }
