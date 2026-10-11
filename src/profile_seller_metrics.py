from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = PROJECT_ROOT / "data" / "raw"


def load_data(filename: str) -> pd.DataFrame:
    path = RAW_DATA / filename

    if not path.exists():
        raise FileNotFoundError(f"Required data file not found: {path}")

    return pd.read_csv(path)


def main() -> None:
    sellers = load_data("olist_sellers_dataset.csv")
    items = load_data("olist_order_items_dataset.csv")
    orders = load_data("olist_orders_dataset.csv")
    reviews = load_data("olist_order_reviews_dataset.csv")

    print("=== Seller Coverage ===")
    item_sellers = set(items["seller_id"].dropna())
    all_sellers = set(sellers["seller_id"].dropna())

    sellers_with_items = all_sellers & item_sellers

    print(f"Total sellers: {len(all_sellers):,}")
    print(f"Sellers with order items: {len(sellers_with_items):,}")
    print(f"Sellers without order items: {len(all_sellers - item_sellers):,}")

    print("\n=== Seller-Order Grain ===")
    seller_orders = items[["seller_id", "order_id"]].drop_duplicates()

    print(f"Order-item rows: {len(items):,}")
    print(f"Distinct seller-order pairs: {len(seller_orders):,}")
    print(f"Distinct orders in order items: {items['order_id'].nunique():,}")

    seller_order_counts = seller_orders.groupby("seller_id")["order_id"].nunique()

    print(f"Sellers with at least one order: {len(seller_order_counts):,}")
    print(f"Median orders per active seller: {seller_order_counts.median():.1f}")
    print(f"Maximum orders for one seller: {seller_order_counts.max():,}")

    print("\n=== Sales Value ===")
    print(f"Missing item prices: {items['price'].isna().sum():,}")
    print(f"Negative item prices: {(items['price'] < 0).sum():,}")
    print(f"Total item price value: {items['price'].sum():,.2f}")
    print(f"Total freight value: {items['freight_value'].sum():,.2f}")

    print("\n=== Order Status and Delivery Dates ===")
    print("Order status counts:")
    print(orders["order_status"].value_counts(dropna=False).to_string())

    delivered = orders["order_status"].eq("delivered")
    delivered_at = pd.to_datetime(
        orders["order_delivered_customer_date"], errors="coerce"
    )
    estimated_at = pd.to_datetime(
        orders["order_estimated_delivery_date"], errors="coerce"
    )

    print(f"Delivered orders: {delivered.sum():,}")
    print(
        "Delivered orders with actual delivery date: "
        f"{(delivered & delivered_at.notna()).sum():,}"
    )
    print(
        "Delivered orders with actual and estimated dates: "
        f"{(delivered & delivered_at.notna() & estimated_at.notna()).sum():,}"
    )

    print("\n=== Review Coverage ===")
    reviews_per_order = reviews.groupby("order_id").size()

    print(f"Review rows: {len(reviews):,}")
    print(f"Orders with reviews: {reviews['order_id'].nunique():,}")
    print(f"Orders with multiple review rows: {(reviews_per_order > 1).sum():,}")
    print(f"Missing review scores: {reviews['review_score'].isna().sum():,}")

    print("\n=== Diagnostic Completed ===")


if __name__ == "__main__":
    main()