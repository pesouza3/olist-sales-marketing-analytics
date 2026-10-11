from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = PROJECT_ROOT / "data" / "raw"


def load_data(filename: str) -> pd.DataFrame:
    return pd.read_csv(RAW_DATA / filename)


def main() -> None:
    items = load_data("olist_order_items_dataset.csv")
    orders = load_data("olist_orders_dataset.csv")
    reviews = load_data("olist_order_reviews_dataset.csv")

    seller_orders = items[["seller_id", "order_id"]].drop_duplicates()

    print("=== Review Aggregation ===")

    review_scores = reviews.groupby("order_id").agg(
        review_rows=("review_score", "size"),
        distinct_scores=("review_score", "nunique"),
        average_review_score=("review_score", "mean"),
    )

    print(f"Review rows: {len(reviews):,}")
    print(f"Distinct reviewed orders: {len(review_scores):,}")
    print(
        "Orders with multiple review rows: "
        f"{(review_scores['review_rows'] > 1).sum():,}"
    )
    print(
        "Orders with different scores across review rows: "
        f"{(review_scores['distinct_scores'] > 1).sum():,}"
    )

    seller_review_pairs = seller_orders.merge(
        review_scores[["average_review_score"]],
        left_on="order_id",
        right_index=True,
        how="inner",
    )

    print(f"Seller-order pairs: {len(seller_orders):,}")
    print(f"Seller-order pairs with reviews: {len(seller_review_pairs):,}")
    print(
        "Distinct sellers represented in review pairs: "
        f"{seller_review_pairs['seller_id'].nunique():,}"
    )

    print("\n=== Delivery Metric Eligibility ===")

    order_dates = orders[
        [
            "order_id",
            "order_status",
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ]
    ].copy()

    date_columns = [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in date_columns:
        order_dates[column] = pd.to_datetime(
            order_dates[column], errors="coerce"
        )

    eligible = (
        order_dates["order_status"].eq("delivered")
        & order_dates["order_delivered_customer_date"].notna()
        & order_dates["order_estimated_delivery_date"].notna()
        & order_dates["order_purchase_timestamp"].notna()
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

    print(f"All orders: {len(order_dates):,}")
    print(f"Eligible delivered orders: {len(eligible_orders):,}")
    print(
        "Orders with negative delivery duration: "
        f"{(eligible_orders['delivery_days'] < 0).sum():,}"
    )
    print(
        "Overall on-time delivery rate: "
        f"{eligible_orders['on_time'].mean():.2%}"
    )
    print(
        "Average delivery duration in days: "
        f"{eligible_orders['delivery_days'].mean():.2f}"
    )

    print("\n=== Check Completed ===")


if __name__ == "__main__":
    main()