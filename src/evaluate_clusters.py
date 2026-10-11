from pathlib import Path

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "seller_clustering_features.csv"


def main() -> None:
    features = pd.read_csv(INPUT_PATH)

    seller_ids = features["seller_id"]
    X = features.drop(columns=["seller_id"])

    if X.isna().any().any():
        raise ValueError("Clustering features contain missing values.")

    print("=== K-Means Cluster Evaluation ===")
    print(f"Sellers: {len(features):,}")
    print(f"Features: {X.shape[1]:,}")
    print("\n k | Silhouette | Smallest cluster | Largest cluster")
    print("-" * 55)

    for k in range(2, 9):
        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10,
        )

        labels = model.fit_predict(X)
        sizes = pd.Series(labels).value_counts()

        score = silhouette_score(X, labels)

        print(
            f"{k:2d} | {score:10.4f} | "
            f"{sizes.min():15,} | {sizes.max():14,}"
        )

    print("\nEvaluation completed.")


if __name__ == "__main__":
    main()