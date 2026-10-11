from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = PROJECT_ROOT / "data" / "raw"


def main() -> None:
    closed_deals = pd.read_csv(
        RAW_DATA / "olist_closed_deals_dataset.csv"
    )
    sellers = pd.read_csv(
        RAW_DATA / "olist_sellers_dataset.csv"
    )

    print("=== Closed Deals: Seller ID Coverage ===")
    print(f"Closed-deal rows: {len(closed_deals):,}")
    print(
        "Missing seller_id values: "
        f"{closed_deals['seller_id'].isna().sum():,}"
    )
    print(
        "Distinct non-null seller IDs: "
        f"{closed_deals['seller_id'].nunique():,}"
    )

    seller_ids = set(sellers["seller_id"].dropna())
    matched = closed_deals["seller_id"].isin(seller_ids)

    print(f"Matched closed-deal rows: {matched.sum():,}")
    print(f"Unmatched closed-deal rows: {(~matched).sum():,}")

    unmatched_ids = (
        closed_deals.loc[~matched, "seller_id"]
        .dropna()
        .drop_duplicates()
    )

    print(
        "Distinct unmatched non-null seller IDs: "
        f"{len(unmatched_ids):,}"
    )

    print("\n=== Closed Deals Columns ===")
    print(closed_deals.columns.tolist())

    print("\n=== Sample Unmatched Records ===")
    print(
        closed_deals.loc[
            ~matched,
            ["mql_id", "seller_id", "sdr_id", "sr_id", "won_date"],
        ].head(10).to_string(index=False)
    )


if __name__ == "__main__":
    main()