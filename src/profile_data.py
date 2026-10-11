
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data/raw")


def profile_csv(file_path: Path) -> None:
    """Report row counts, columns, and missing-value percentages."""
    df = pd.read_csv(file_path)

    print(f"\n{'=' * 60}")
    print(f"Table: {file_path.name}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    missing = df.isna().mean().mul(100)
    missing = missing[missing > 0].sort_values(ascending=False)

    if missing.empty:
        print("Missing values: none")
    else:
        print("Columns with missing values (%):")
        print(missing.round(2).to_string())


def main() -> None:
    for file_path in sorted(DATA_DIR.glob("*.csv")):
        profile_csv(file_path)


if __name__ == "__main__":
    main()
