# -*- coding: utf-8 -*-
"""Module for high-level automation tasks."""

from pathlib import Path

import pandas as pd
from numbers_parser import Document

from transform.date_transform import expand_date_column


def _read_file(file_path: str | Path) -> pd.DataFrame:
    """Read a file into a pandas DataFrame based on its extension."""
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"No such file or directory: '{file_path}'")

    if file_path.suffix == ".csv":
        return pd.read_csv(file_path)
    if file_path.suffix == ".xlsx":
        return pd.read_excel(file_path)
    if file_path.suffix == ".numbers":
        doc = Document(file_path)
        sheet = doc.sheets[0]
        data = [row for row in sheet.tables[0].rows(values_only=True)]
        return pd.DataFrame(data[1:], columns=data[0])

    raise ValueError(f"Unsupported file type: '{file_path.suffix}'")


def _find_date_columns(df: pd.DataFrame, sample_size: int = 100) -> list[str]:
    """Attempt to find date-like columns in a DataFrame."""
    date_columns = []
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                # Attempt to convert a sample of the column to datetime
                sample = df[col].dropna().head(sample_size)
                if sample.empty:
                    continue
                pd.to_datetime(sample, errors="raise")
                date_columns.append(col)
            except (ValueError, TypeError):
                # This column is not consistently convertible to date
                continue
    return date_columns


def process_file_dates(
    file_path: str, prefix: str = "_transform_date"
) -> str:
    """Read a file, process all date columns, and save to a new CSV.

    This function reads a CSV, XLSX, or Numbers file, automatically finds
    any columns containing dates, and expands them into year, month, day,
    day of the week, and day of the year. The original date column is
    removed, and the result is saved to a new CSV file.

    Args:
        file_path: The path to the input file.
        prefix: The prefix to add to the new filename.

    Returns:
        The path to the newly created CSV file.
    """
    df = _read_file(file_path)
    date_columns = _find_date_columns(df)

    if not date_columns:
        print("No date columns found to transform.")
        return ""

    for col_name in date_columns:
        df = expand_date_column(df, col_name, drop_original=True)

    original_path = Path(file_path)
    new_filename = f"{original_path.stem}{prefix}.csv"
    new_filepath = original_path.parent / new_filename
    df.to_csv(new_filepath, index=False)

    return str(new_filepath)
