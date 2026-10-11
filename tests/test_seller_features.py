import pandas as pd

from src.build_seller_features import build_seller_features


def test_one_row_per_seller():
    features = build_seller_features()

    assert len(features) == 3095
    assert features["seller_id"].notna().all()
    assert features["seller_id"].is_unique


def test_commercial_metrics_are_nonnegative():
    features = build_seller_features()

    columns = [
        "order_count",
        "items_sold",
        "total_sales_value",
        "average_order_value",
    ]

    assert features[columns].notna().all().all()
    assert (features[columns] >= 0).all().all()


def test_review_scores_are_in_valid_range():
    features = build_seller_features()

    observed = features["average_review_score"].dropna()

    assert observed.between(1, 5).all()


def test_delivery_rates_are_in_valid_range():
    features = build_seller_features()

    observed = features["on_time_delivery_rate"].dropna()

    assert observed.between(0, 1).all()


def test_delivery_duration_is_nonnegative():
    features = build_seller_features()

    observed = features["average_delivery_days"].dropna()

    assert (observed >= 0).all()
