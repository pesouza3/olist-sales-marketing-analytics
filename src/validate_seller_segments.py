from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"


def main() -> None:
    segments = pd.read_csv(PROCESSED_DATA / "seller_segments.csv")
    features = pd.read_csv(PROCESSED_DATA / "seller_features.csv")

    data = segments.merge(
        features[
            [
                "seller_id",
                "average_review_score",
                "on_time_delivery_rate",
                "average_delivery_days",
            ]
        ],
        on="seller_id",
        how="left",
        suffixes=("", "_source"),
        validate="one_to_one",
    )

    # Delivery observation counts at seller-order level.
    items = pd.read_csv(PROCESSED_DATA.parent / "raw" / "olist_order_items_dataset.csv")
    orders = pd.read_csv(PROCESSED_DATA.parent / "raw" / "olist_orders_dataset.csv")

    seller_orders = items[["seller_id", "order_id"]].drop_duplicates()

    eligible_orders = orders.loc[
        orders["order_status"].eq("delivered")
        & orders["order_delivered_customer_date"].notna()
        & orders["order_estimated_delivery_date"].notna()
        & orders["order_purchase_timestamp"].notna(),
        ["order_id"],
    ]

    eligible_pairs = seller_orders.merge(
        eligible_orders,
        on="order_id",
        how="inner",
        validate="many_to_one",
    )

    delivery_counts = eligible_pairs.groupby("seller_id").agg(
        eligible_delivery_orders=("order_id", "nunique")
    )

    data = data.merge(
        delivery_counts,
        on="seller_id",
        how="left",
        validate="one_to_one",
    )

    data["eligible_delivery_orders"] = (
        data["eligible_delivery_orders"].fillna(0)
    )

    data["missing_review"] = data["average_review_score"].isna()
    data["missing_delivery"] = data["on_time_delivery_rate"].isna()
    data["low_order_volume"] = data["order_count"] < 5

    print("=== Cluster Reliability Summary ===")

    summary = data.groupby("cluster").agg(
        sellers=("seller_id", "size"),
        median_orders=("order_count", "median"),
        sellers_under_5_orders=("low_order_volume", "sum"),
        missing_review=("missing_review", "sum"),
        missing_delivery=("missing_delivery", "sum"),
        median_eligible_delivery_orders=("eligible_delivery_orders", "median"),
        median_review_score=("average_review_score", "median"),
        median_on_time_rate=("on_time_delivery_rate", "median"),
    )

    summary["pct_under_5_orders"] = (
        summary["sellers_under_5_orders"] / summary["sellers"] * 100
    )
    summary["pct_missing_review"] = (
        summary["missing_review"] / summary["sellers"] * 100
    )
    summary["pct_missing_delivery"] = (
        summary["missing_delivery"] / summary["sellers"] * 100
    )

    print(summary.round(2).to_string())

    print("\n=== Overall Checks ===")
    print(f"Total sellers: {len(data):,}")
    print(f"Unique sellers: {data['seller_id'].nunique():,}")
    print(
        "Sellers with fewer than 5 orders: "
        f"{data['low_order_volume'].sum():,}"
    )
    print(
        "Sellers with no eligible delivery observations: "
        f"{data['missing_delivery'].sum():,}"
    )
    print("\nValidation completed.")


if __name__ == "__main__":
    main()