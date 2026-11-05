"""
NeuroQ-Flood — Live Discharge Forecasting

Trains classical and fixed-weight hybrid models
using recent USGS observations.

Produces a 60-minute forecast from the latest
available observation.

Live adaptive feedback is not yet implemented.
"""

from datetime import datetime, timedelta, timezone

from neuroq.data_source import get_recent_usgs
from neuroq.preprocessing import prepare, fit_ranges
from neuroq.forecasting import (
    DischargeForecaster,
    extract_features,
    calculate_discharge_trends,
    HORIZON_MINUTES,
)
from neuroq.memory import clamp_weights


def run_live_forecast(weights, days=14):

    weights = clamp_weights(weights)

    rows = get_recent_usgs(days=days)

    if len(rows) < 20:
        raise ValueError(
            "Not enough observations for forecasting."
        )

    rows = sorted(
        rows,
        key=lambda row: row["timestamp"]
    )

    # Deduplicate timestamps.
    lookup = {
        row["timestamp"]: row
        for row in rows
    }

    rows = [
        lookup[timestamp]
        for timestamp in sorted(lookup)
    ]

    latest = rows[-1]

    now = datetime.now(timezone.utc)

    forecast_target = (
        latest["timestamp"]
        + timedelta(minutes=HORIZON_MINUTES)
    )

    if forecast_target <= now:
        raise RuntimeError(
            "Latest USGS observation is too old "
            "to generate a genuine live forecast. "
            f"Observation: {latest['timestamp']}, "
            f"target: {forecast_target}, "
            f"current time: {now}"
        )

    # Fit normalization using historical observations.
    # The latest observation is reserved for prediction.
    training_rows = rows[:-1]

    ranges = fit_ranges(training_rows)

    horizon = timedelta(minutes=HORIZON_MINUTES)

    classical_training = []
    hybrid_training = []
    targets = []

    for index, current in enumerate(training_rows):

        future = lookup.get(
            current["timestamp"] + horizon
        )

        if future is None:
            continue

        # Never train on an observation later than
        # the training period.
        if future["timestamp"] > training_rows[-1]["timestamp"]:
            continue

        previous = (
            training_rows[index - 1]
            if index > 0
            else None
        )

        inputs = prepare(
            current,
            previous,
            ranges
        )

        trends, availability = (
            calculate_discharge_trends(
                current,
                lookup
            )
        )

        classical_training.append(
            extract_features(
                inputs,
                weights,
                current["discharge_cfs"],
                trends,
                availability,
                include_quantum=False
            )
        )

        hybrid_training.append(
            extract_features(
                inputs,
                weights,
                current["discharge_cfs"],
                trends,
                availability,
                include_quantum=True
            )
        )

        targets.append(
            future["discharge_cfs"]
        )

    if len(targets) < 10:
        raise ValueError(
            "Not enough complete training examples."
        )

    classical_model = DischargeForecaster()
    hybrid_model = DischargeForecaster()

    classical_model.fit(
        classical_training,
        targets
    )

    hybrid_model.fit(
        hybrid_training,
        targets
    )

    # Prepare latest observation.
    previous = rows[-2]

    inputs = prepare(
        latest,
        previous,
        ranges
    )

    trends, availability = (
        calculate_discharge_trends(
            latest,
            lookup
        )
    )

    classical_features = extract_features(
        inputs,
        weights,
        latest["discharge_cfs"],
        trends,
        availability,
        include_quantum=False
    )

    hybrid_features = extract_features(
        inputs,
        weights,
        latest["discharge_cfs"],
        trends,
        availability,
        include_quantum=True
    )

    classical_prediction = classical_model.predict(
        classical_features
    )

    hybrid_prediction = hybrid_model.predict(
        hybrid_features
    )

    return {
        "station": "08074000",
        "observation_time": latest["timestamp"],
        "forecast_time": latest["timestamp"] + horizon,
        "gage_height_ft": latest["gage_height_ft"],
        "current_discharge_cfs": latest["discharge_cfs"],
        "persistence_forecast_cfs": latest["discharge_cfs"],
        "classical_forecast_cfs": classical_prediction,
        "hybrid_forecast_cfs": hybrid_prediction,
        "training_examples": len(targets),
        "measurements": len(rows),
        "weights": weights,
        "inputs": inputs,
        "trends": trends,
        "availability": availability,
        "model_state": {
        "coefficients": hybrid_model.coefficients,
        "means": hybrid_model.means,
        "scales": hybrid_model.scales,
},
    }