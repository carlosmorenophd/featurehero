"""Functions for data transformation tasks."""
import os
import pandas as pd


def _read_file(file_path: str) -> pd.DataFrame:
    """Reads a file into a pandas DataFrame based on its extension."""
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.csv':
        return pd.read_csv(file_path)
    if file_extension.lower() in ['.xls', '.xlsx']:
        return pd.read_excel(file_path)
    # Note: .numbers support is more complex and is omitted here for brevity.
    # It would require logic similar to work_space_file.py
    raise ValueError(f"Unsupported file type: {file_extension}")


def transform_data(file_path: str, transform_type: str, columns: list[str],
                   out_filename: str | None):
    """
    Transforms data in a file based on the specified type and columns.

    Args:
        file_path (str): Path to the input data file.
        transform_type (str): The type of transformation
                              to apply ('date' or 'category').
        columns (list[str]): A list of column names to transform.
        out_filename (str | None): New name for the output file. If None, a
                                   default name is generated.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df = _read_file(file_path)

    # Validate that all specified columns exist in the DataFrame
    missing_cols = [col for col in columns if col not in df.columns]
    if missing_cols:
        raise ValueError(
            f"The following columns were not found in the file: "
            f"{', '.join(missing_cols)}")

    if transform_type == 'date':
        for col in columns:
            # Convert column to datetime
            date_col = pd.to_datetime(df[col], errors='coerce')
            # Extract features
            df[f'{col}_year'] = date_col.dt.year
            df[f'{col}_month'] = date_col.dt.month
            df[f'{col}_day'] = date_col.dt.day
            df[f'{col}_dayofweek'] = date_col.dt.dayofweek
            df[f'{col}_dayofyear'] = date_col.dt.dayofyear
            # Drop original column
            df = df.drop(columns=[col])
        print(
            f"Applied 'date' transformation to columns: {', '.join(columns)}")

    elif transform_type == 'category':
        for col in columns:
            # Convert column to categorical
            # and get integer codes (starts from 0)
            # We add 1 to make it start from 1 as requested.
            df[f'{col}_number'] = pd.Categorical(df[col]).codes + 1
            df = df.drop(columns=[col])
        print(
            "Applied 'category' (label encoding) transformation to columns: "
            f"{', '.join(columns)}"
        )

    # Determine output filename and path
    if out_filename is None:
        base, _ = os.path.splitext(os.path.basename(file_path))
        out_filename = f"{base}_transformed.csv"

    # Ensure output is saved as .csv for consistency
    if not out_filename.lower().endswith('.csv'):
        out_filename += '.csv'

    output_dir = os.path.dirname(file_path)
    out_path = os.path.join(output_dir, out_filename)

    df.to_csv(out_path, index=False)
    print(f"Transformed file saved to: {out_path}")
