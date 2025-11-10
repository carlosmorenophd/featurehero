# -*- coding: utf-8 -*-
"""Module to transform date columns in a pandas DataFrame."""

import pandas as pd


def expand_date_column(
    df: pd.DataFrame, column_name: str, drop_original: bool = False
) -> pd.DataFrame:
    """Transform a date column into multiple time-based features.

    Expands the specified column into year, month, day, day of week,
    week of year, and day of year.

    Args:
        df: The input pandas DataFrame.
        column_name: The name of the column containing date/datetime objects.
        drop_original: If True, the original date column will be dropped.

    Returns:
        A pandas DataFrame with the new date-based feature columns.

    Raises:
        KeyError: If the specified column_name does not exist in the DataFrame.
        TypeError: If the specified column cannot be converted to datetime.
    """
    if column_name not in df.columns:
        raise KeyError(f"Column '{column_name}' not found in the DataFrame.")

    # Ensure the column is of datetime type
    date_col = pd.to_datetime(df[column_name], errors="coerce")

    df[f"{column_name}_year"] = date_col.dt.year
    df[f"{column_name}_month"] = date_col.dt.month
    df[f"{column_name}_day"] = date_col.dt.day
    df[f"{column_name}_day_of_week"] = date_col.dt.dayofweek  # Monday=0, Sunday=6
    df[f"{column_name}_week_of_year"] = date_col.dt.isocalendar().week
    df[f"{column_name}_day_of_year"] = date_col.dt.dayofyear

    if drop_original:
        df = df.drop(columns=[column_name])

    return df
