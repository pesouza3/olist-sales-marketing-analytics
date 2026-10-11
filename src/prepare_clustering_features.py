from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

INPUT_PATH = PROCESSED_DATA / "seller_features.csv"
OUTPUT_PATH = PROCESSED_DATA / "seller_clustering_features.csv"

LOG_COLUMNS = [
    "order_count",
    "items_sold",
    "total_sales_value",
    "average_order_value",
]

METRIC_COLUMNS = [
    "average_review_score",
    "on_time_delivery_rate",
    "average_delivery_days",
]


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Run src/build_seller_features.py first: {INPUT_PATH}"
        )

    features = pd.read_csv(INPUT_PATH)

    if features["seller_id"].isna().any():
        raise ValueError("seller_id contains missing values.")

    if not features["seller_id"].is_unique:
        raise ValueError("Expected exactly one row per seller.")

    model_features = features[LOG_COLUMNS + METRIC_COLUMNS].copy()

    # Reduce right-skew in nonnegative commercial features.
    for column in LOG_COLUMNS:
        if (model_features[column] < 0).any():
            raise ValueError(f"{column} contains negative values.")

        model_features[column] = np.log1p(model_features[column])

    # Cap extreme delivery durations for clustering only.
    delivery_cap = model_features["average_delivery_days"].quantile(0.99)
    model_features["average_delivery_days"] = (
        model_features["average_delivery_days"].clip(upper=delivery_cap)
    )

    # Preserve the original data; impute only the modeling input.
    imputer = SimpleImputer(strategy="median")
    imputed = imputer.fit_transform(model_features)

    prepared = pd.DataFrame(
        imputed,
        columns=model_features.columns,
        index=model_features.index,
    )

    scaler = StandardScaler()
    scaled = scaler.fit_transform(prepared)

    output = pd.DataFrame(
        scaled,
        columns=prepared.columns,
        index=prepared.index,
    )

    output.insert(0, "seller_id", features["seller_id"])

    PROCESSED_DATA.mkdir(parents=True, exist_ok=True)
    output.to_csv(OUTPUT_PATH, index=False)

    print("=== Clustering Features Prepared ===")
    print(f"Input sellers: {len(features):,}")
    print(f"Output sellers: {len(output):,}")
    print(f"Feature columns: {len(prepared.columns):,}")
    print(f"Delivery-duration 99th percentile cap: {delivery_cap:.2f} days")
    print(f"Missing values after imputation: {int(output.isna().sum().sum()):,}")
    print(f"Duplicate seller IDs: {output['seller_id'].duplicated().sum():,}")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()