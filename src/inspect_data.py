
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data/raw")


def inspect_csv(file_path: Path) -> None:
    """Print the structure of a CSV without loading the full dataset."""
    df = pd.read_csv(file_path, nrows=5)

    with file_path.open("r", encoding="utf-8-sig") as file:
        header = file.readline().strip()

    columns = list(df.columns)

    print(f"\n{'=' * 70}")
    print(f"File: {file_path.name}")
    print(f"Columns: {len(columns)}")
    print(f"Column names: {', '.join(columns)}")
    print("Sample (first 5 rows):")
    print(df.to_string(index=False))


def main() -> None:
    csv_files = sorted(DATA_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {DATA_DIR.resolve()}")

    print(f"Inspecting {len(csv_files)} CSV files")

    for file_path in csv_files:
        inspect_csv(file_path)


if __name__ == "__main__":
    main()
