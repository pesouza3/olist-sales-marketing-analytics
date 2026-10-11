from pathlib import Path

import pandas as pd
from sklearn.cluster import KMeans


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

FEATURES_PATH = PROCESSED_DATA / "seller_clustering_features.csv"
METRICS_PATH = PROCESSED_DATA / "seller_features.csv"


def main() -> None:
    clustering_features = pd.read_csv(FEATURES_PATH)
    original_features = pd.read_csv(METRICS_PATH)

    X = clustering_features.drop(columns=["seller_id"])

    model = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10,
    )

    clustered = clustering_features[["seller_id"]].copy()
    clustered["cluster"] = model.fit_predict(X)

    results = original_features.merge(
        clustered,
        on="seller_id",
        how="inner",
        validate="one_to_one",
    )

    output_path = PROCESSED_DATA / "seller_segments.csv"
    results.to_csv(output_path, index=False)

    print("=== Seller Segment Sizes ===")
    print(
        results["cluster"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    metrics = [
        "order_count",
        "items_sold",
        "total_sales_value",
        "average_order_value",
        "average_review_score",
        "on_time_delivery_rate",
        "average_delivery_days",
    ]

    summary = results.groupby("cluster")[metrics].agg(
        ["median", "mean"]
    ).round(2)

    print("\n=== Segment Profiles: Median and Mean ===")
    print(summary.to_string())

    print(f"\nOutput saved to: {output_path}")


if __name__ == "__main__":
    main()