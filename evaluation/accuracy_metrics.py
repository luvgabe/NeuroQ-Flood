"""
NeuroQ-Flood — Forecast Accuracy Metrics

Evaluates numerical discharge forecasts
against observed historical discharge.
"""

import math


def metrics(observed, predicted):

    if len(observed) != len(predicted):
        raise ValueError(
            "Observed and predicted lengths differ."
        )

    if not observed:
        raise ValueError(
            "No predictions available for evaluation."
        )

    count = len(observed)

    errors = [
        prediction - actual
        for actual, prediction
        in zip(observed, predicted)
    ]

    mae = sum(
        abs(error)
        for error in errors
    ) / count

    rmse = math.sqrt(
        sum(
            error ** 2
            for error in errors
        ) / count
    )

    mean_observed = (
        sum(observed) / count
    )

    denominator = sum(
        (value - mean_observed) ** 2
        for value in observed
    )

    numerator = sum(
        error ** 2
        for error in errors
    )

    nse = (
        1.0 - numerator / denominator
        if denominator > 0
        else None
    )

    observed_peak = max(observed)
    predicted_peak = max(predicted)

    peak_error = (
        100.0
        * (
            predicted_peak - observed_peak
        )
        / observed_peak
        if observed_peak != 0
        else None
    )

    return {

        "count": count,

        "MAE": mae,

        "RMSE": rmse,

        "NSE": nse,

        "peak_flow_error_percent": peak_error

    }


def print_metrics(title, result):

    print(f"\n{title}")
    print("-" * 45)

    print(
        f"Evaluated forecasts: "
        f"{result['count']}"
    )

    print(
        f"MAE: {result['MAE']:.3f} cfs"
    )

    print(
        f"RMSE: {result['RMSE']:.3f} cfs"
    )

    nse = result["NSE"]

    print(
        "NSE: "
        + (
            f"{nse:.4f}"
            if nse is not None
            else "N/A"
        )
    )

    peak = result[
        "peak_flow_error_percent"
    ]

    print(
        "Peak-flow error: "
        + (
            f"{peak:.2f}%"
            if peak is not None
            else "N/A"
        )
    )