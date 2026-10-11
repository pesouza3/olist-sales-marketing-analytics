from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"


def load_data(filename: str) -> pd.DataFrame:
    path = RAW_DATA / filename

    if not path.exists():
        raise FileNotFoundError(f"Required data file not found: {path}")

    return pd.read_csv(path)


def build_seller_features() -> pd.DataFrame:
    sellers = load_data("olist_sellers_dataset.csv")
    items = load_data("olist_order_items_dataset.csv")
    orders = load_data("olist_orders_dataset.csv")
    reviews = load_data("olist_order_reviews_dataset.csv")

    # One row per seller-order pair for order-level seller metrics.
    seller_orders = items[["seller_id", "order_id"]].drop_duplicates()

    # Aggregate item-level metrics separately.
    sales = items.groupby("seller_id").agg(
        items_sold=("order_id", "size"),
        total_sales_value=("price", "sum"),
    )

    seller_order_counts = (
        seller_orders.groupby("seller_id")
        .agg(order_count=("order_id", "nunique"))
    )

    # Average item sales value per seller-order pair.
    average_order_value = (
        sales["total_sales_value"]
        .div(seller_order_counts["order_count"])
        .rename("average_order_value")
    )

    # Aggregate reviews to one record per order before joining.
    order_reviews = reviews.groupby("order_id").agg(
        average_review_score=("review_score", "mean")
    )

    seller_reviews = seller_orders.merge(
        order_reviews,
        left_on="order_id",
        right_index=True,
        how="inner",
    )

    seller_review_scores = seller_reviews.groupby("seller_id").agg(
        average_review_score=("average_review_score", "mean")
    )

    # Calculate delivery metrics at order level.
    order_dates = orders[
        [
            "order_id",
            "order_status",
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ]
    ].copy()

    for column in [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]:
        order_dates[column] = pd.to_datetime(
            order_dates[column], errors="coerce"
        )

    eligible = (
        order_dates["order_status"].eq("delivered")
        & order_dates["order_purchase_timestamp"].notna()
        & order_dates["order_delivered_customer_date"].notna()
        & order_dates["order_estimated_delivery_date"].notna()
    )

    eligible_orders = order_dates.loc[eligible].copy()

    eligible_orders["delivery_days"] = (
        eligible_orders["order_delivered_customer_date"]
        - eligible_orders["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    eligible_orders["on_time"] = (
        eligible_orders["order_delivered_customer_date"]
        <= eligible_orders["order_estimated_delivery_date"]
    )

    # Connect eligible order metrics to each seller-order pair.
    seller_delivery = seller_orders.merge(
        eligible_orders[
            ["order_id", "delivery_days", "on_time"]
        ],
        on="order_id",
        how="inner",
        validate="many_to_one",
    )

    seller_delivery_metrics = seller_delivery.groupby("seller_id").agg(
        on_time_delivery_rate=("on_time", "mean"),
        average_delivery_days=("delivery_days", "mean"),
    )

    # Start from the complete seller population.
    features = sellers[["seller_id"]].copy()

    features = features.merge(
        seller_order_counts,
        left_on="seller_id",
        right_index=True,
        how="left",
        validate="one_to_one",
    )

    features = features.merge(
        sales,
        left_on="seller_id",
        right_index=True,
        how="left",
        validate="one_to_one",
    )

    features = features.merge(
        average_order_value,
        left_on="seller_id",
        right_index=True,
        how="left",
        validate="one_to_one",
    )

    features = features.merge(
        seller_review_scores,
        left_on="seller_id",
        right_index=True,
        how="left",
        validate="one_to_one",
    )

    features = features.merge(
        seller_delivery_metrics,
        left_on="seller_id",
        right_index=True,
        how="left",
        validate="one_to_one",
    )

    # Count and sales metrics are zero only if no source records exist.
    for column in [
        "order_count",
        "items_sold",
        "total_sales_value",
        "average_order_value",
    ]:
        features[column] = features[column].fillna(0)

    return features


def main() -> None:
    features = build_seller_features()

    PROCESSED_DATA.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DATA / "seller_features.csv"
    features.to_csv(output_path, index=False)

    print("=== Seller Feature Dataset Created ===")
    print(f"Output: {output_path}")
    print(f"Rows: {len(features):,}")
    print(f"Columns: {len(features.columns):,}")
    print(f"Unique sellers: {features['seller_id'].nunique():,}")

    print("\n=== Missing Values ===")
    print(features.isna().sum().to_string())

    print("\n=== Feature Summary ===")
    print(features.drop(columns="seller_id").describe().round(2).to_string())


if __name__ == "__main__":
    main()