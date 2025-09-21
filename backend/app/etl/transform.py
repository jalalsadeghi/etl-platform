# backend/app/etl/transform.py
from typing import Dict, List

import pandas as pd


def clean_rows(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    # Map common fields to our schema
    # jsonplaceholder has: id, name, username, email, ...
    if "name" in df.columns and "email" in df.columns:
        keep = ["id", "name", "email"]
        df = df[[c for c in keep if c in df.columns]]
        df = df.drop_duplicates(subset=["email"]).dropna(subset=["email"])
        df = df.rename(columns={"name": "full_name"})
    else:
        # fallback: just drop empty rows
        df = df.dropna(how="all")
    return df


def to_users_df(rows: List[Dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    # Standardize columns we care about
    # For jsonplaceholder users: id, name, email exist
    cols = {"id": "ext_id", "name": "name", "email": "email"}
    df = df.rename(columns=cols)
    keep = list(cols.values())
    df = df[[c for c in keep if c in df.columns]].copy()
    # Basic cleaning
    df = df.drop_duplicates(subset=["ext_id"]).dropna(subset=["ext_id"])
    return df
