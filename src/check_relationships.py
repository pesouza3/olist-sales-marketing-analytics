from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = PROJECT_ROOT / "data" / "raw"


def load_data(filename: str) -> pd.DataFrame:
    """Load a CSV file from the raw data directory."""
    path = RAW_DATA / filename

    if not path.exists():
        raise FileNotFoundError(f"Required data file not found: {path}")

    return pd.read_csv(path)


def report_unique_key(
    df: pd.DataFrame,
    column: str,
    table_name: str,
) -> None:
    """Report missing and duplicate values in a candidate key."""
    missing = df[column].isna().sum()
    duplicates = df[column].duplicated().sum()

    print(f"\n{table_name}.{column}")
    print(f"  Rows: {len(df):,}")
    print(f"  Missing values: {missing:,}")
    print(f"  Duplicate values: {duplicates:,}")


def report_unmatched_keys(
    source: pd.DataFrame,
    source_column: str,
    target: pd.DataFrame,
    target_column: str,
    relationship_name: str,
) -> None:
    """Report source records without a matching target key."""
    target_keys = set(target[target_column].dropna())
    unmatched = ~source[source_column].isin(target_keys)

    print(f"\n{relationship_name}")
    print(f"  Source rows: {len(source):,}")
    print(f"  Unmatched source rows: {unmatched.sum():,}")
    print(
        "  Unmatched distinct keys: "
        f"{source.loc[unmatched, source_column].nunique():,}"
    )


def main() -> None:
    orders = load_data("olist_orders_dataset.csv")
    order_items = load_data("olist_order_items_dataset.csv")
    sellers = load_data("olist_sellers_dataset.csv")
    reviews = load_data("olist_order_reviews_dataset.csv")
    closed_deals = load_data("olist_closed_deals_dataset.csv")

    print("=== Candidate Key Checks ===")
    report_unique_key(orders, "order_id", "orders")
    report_unique_key(sellers, "seller_id", "sellers")
    report_unique_key(closed_deals, "mql_id", "closed_deals")

    print("\n=== Referential Integrity Checks ===")
    report_unmatched_keys(
        order_items,
        "order_id",
        orders,
        "order_id",
        "Order items -> Orders",
    )
    report_unmatched_keys(
        order_items,
        "seller_id",
        sellers,
        "seller_id",
        "Order items -> Sellers",
    )
    report_unmatched_keys(
        reviews,
        "order_id",
        orders,
        "order_id",
        "Reviews -> Orders",
    )
    report_unmatched_keys(
        closed_deals,
        "seller_id",
        sellers,
        "seller_id",
        "Closed deals -> Sellers",
    )

    print("\n=== Order Structure ===")
    sellers_per_order = order_items.groupby("order_id")["seller_id"].nunique()
    multi_seller_orders = (sellers_per_order > 1).sum()

    print(f"Orders represented in order items: {len(sellers_per_order):,}")
    print(f"Orders with multiple sellers: {multi_seller_orders:,}")
    print(
        "Maximum distinct sellers in one order: "
        f"{sellers_per_order.max():,}"
    )

    print("\n=== Checks Completed ===")


if __name__ == "__main__":
    main()