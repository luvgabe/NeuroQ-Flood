"""
NeuroQ-Flood — Historical Replay
Week 10: Classical vs. Quantum Forecasting

Replays historical USGS measurements chronologically.

Evaluates three forecasting approaches:

1. Persistence baseline
2. Classical forecasting
3. Hybrid quantum-classical forecasting

All models use the same chronological training
and testing periods.

Forecasts are evaluated 60 minutes ahead.
"""

import csv

from datetime import timedelta
from pathlib import Path

from neuroq.preprocessing import (
    prepare,
    fit_ranges
)

from neuroq.risk_assessment import analyze

from neuroq.memory import clamp_weights

from neuroq.forecasting import (
    DischargeForecaster,
    extract_features,
    calculate_discharge_trends,
    HORIZON_MINUTES
)

from evaluation.accuracy_metrics import metrics


def replay(rows, weights, destination):

    weights = clamp_weights(weights)

    rows = sorted(
        rows,
        key=lambda row: row["timestamp"]
    )

    # Remove duplicate timestamps.

    unique_rows = []

    for row in rows:

        if (
            unique_rows
            and row["timestamp"]
            <= unique_rows[-1]["timestamp"]
        ):
            continue

        unique_rows.append(row)

    rows = unique_rows

    if len(rows) < 20:
        raise ValueError(
            "At least 20 historical measurements "
            "are required."
        )

    destination = Path(destination)

    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Chronological training/test split.

    split = int(len(rows) * 0.60)

    training_rows = rows[:split]

    ranges = fit_ranges(training_rows)

    lookup = {
        row["timestamp"]: row
        for row in rows
    }

    horizon = timedelta(
        minutes=HORIZON_MINUTES
    )

    # Prepare training datasets.

    classical_training = []

    hybrid_training = []

    targets = []

    for index, current in enumerate(
        training_rows
    ):

        future_time = (
            current["timestamp"] + horizon
        )

        future = lookup.get(future_time)

        if future is None:
            continue

        # Prevent training targets from
        # crossing into the test period.

        if (
            future["timestamp"]
            > training_rows[-1]["timestamp"]
        ):
            continue

        previous = (
            rows[index - 1]
            if index > 0
            else None
        )

        inputs = prepare(
            current,
            previous,
            ranges
        )

        # Only measurements at or before
        # the current timestamp are used.

        trends, availability = (
            calculate_discharge_trends(
                current,
                lookup
            )
        )

        classical_features = extract_features(
            inputs,
            weights,
            current["discharge_cfs"],
            trends,
            availability,
            include_quantum=False
        )

        hybrid_features = extract_features(
            inputs,
            weights,
            current["discharge_cfs"],
            trends,
            availability,
            include_quantum=True
        )

        classical_training.append(
            classical_features
        )

        hybrid_training.append(
            hybrid_features
        )

        targets.append(
            future["discharge_cfs"]
        )

    if len(targets) < 10:
        raise ValueError(
            "Not enough complete training examples."
        )

    # Train both forecasting models.

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

    columns = [

        "timestamp",
        "dataset_split",

        "gage_height_ft",
        "discharge_cfs",

        "gage_norm",
        "discharge_norm",
        "rise_norm",

        "trend_15min_cfs",
        "trend_30min_cfs",
        "trend_60min_cfs",

        "trend_15min_available",
        "trend_30min_available",
        "trend_60min_available",

        "quantum_score",
        "classical_score",
        "hybrid_score",

        "risk",
        "recommendation",

        "gage_weight",
        "discharge_weight",
        "change_weight",

        "forecast_horizon_minutes",
        "forecast_timestamp",

        "actual_future_discharge_cfs",

        "persistence_forecast_cfs",
        "classical_forecast_cfs",
        "hybrid_forecast_cfs",

        "classical_absolute_error_cfs",
        "hybrid_absolute_error_cfs",
        "persistence_absolute_error_cfs"

    ]

    observed = []

    persistence_predictions = []
    classical_predictions = []
    hybrid_predictions = []

    with destination.open(
        "w",
        newline=""
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=columns
        )

        writer.writeheader()

        previous = None

        for index, current in enumerate(rows):

            inputs = prepare(
                current,
                previous,
                ranges
            )

            risk_result = analyze(
                inputs,
                weights
            )

            trends, availability = (
                calculate_discharge_trends(
                    current,
                    lookup
                )
            )

            classical_features = extract_features(
                inputs,
                weights,
                current["discharge_cfs"],
                trends,
                availability,
                include_quantum=False
            )

            hybrid_features = extract_features(
                inputs,
                weights,
                current["discharge_cfs"],
                trends,
                availability,
                include_quantum=True
            )

            classical_prediction = (
                classical_model.predict(
                    classical_features
                )
            )

            hybrid_prediction = (
                hybrid_model.predict(
                    hybrid_features
                )
            )

            persistence_prediction = (
                current["discharge_cfs"]
            )

            future_time = (
                current["timestamp"] + horizon
            )

            future = lookup.get(
                future_time
            )

            actual = (
                future["discharge_cfs"]
                if future is not None
                else None
            )

            is_test = index >= split

            if is_test and actual is not None:

                observed.append(actual)

                persistence_predictions.append(
                    persistence_prediction
                )

                classical_predictions.append(
                    classical_prediction
                )

                hybrid_predictions.append(
                    hybrid_prediction
                )

            def absolute_error(prediction):

                if actual is None:
                    return ""

                return round(
                    abs(prediction - actual),
                    5
                )

            writer.writerow({

                "timestamp":
                    current["timestamp"].isoformat(),

                "dataset_split":
                    "TEST" if is_test else "TRAIN",

                "gage_height_ft":
                    current["gage_height_ft"],

                "discharge_cfs":
                    current["discharge_cfs"],

                "gage_norm":
                    round(inputs["gage_height"], 5),

                "discharge_norm":
                    round(inputs["discharge"], 5),

                "rise_norm":
                    round(inputs["water_change"], 5),

                "trend_15min_cfs":
                    trends[15],

                "trend_30min_cfs":
                    trends[30],

                "trend_60min_cfs":
                    trends[60],

                "trend_15min_available":
                    availability[15],

                "trend_30min_available":
                    availability[30],

                "trend_60min_available":
                    availability[60],

                "quantum_score":
                    round(
                        risk_result["quantum_score"],
                        5
                    ),

                "classical_score":
                    round(
                        risk_result["classical_score"],
                        5
                    ),

                "hybrid_score":
                    round(
                        risk_result["hybrid_score"],
                        5
                    ),

                "risk":
                    risk_result["risk"],

                "recommendation":
                    risk_result["recommendation"],

                **weights,

                "forecast_horizon_minutes":
                    HORIZON_MINUTES,

                "forecast_timestamp":
                    future_time.isoformat(),

                "actual_future_discharge_cfs":
                    actual if actual is not None else "",

                "persistence_forecast_cfs":
                    round(
                        persistence_prediction,
                        5
                    ),

                "classical_forecast_cfs":
                    round(
                        classical_prediction,
                        5
                    ),

                "hybrid_forecast_cfs":
                    round(
                        hybrid_prediction,
                        5
                    ),

                "classical_absolute_error_cfs":
                    absolute_error(
                        classical_prediction
                    ),

                "hybrid_absolute_error_cfs":
                    absolute_error(
                        hybrid_prediction
                    ),

                "persistence_absolute_error_cfs":
                    absolute_error(
                        persistence_prediction
                    )

            })

            previous = current

    if not observed:
        raise ValueError(
            "No matched test forecasts available."
        )

    return {

        "measurements": len(rows),

        "training_examples": len(targets),

        "test_forecasts": len(observed),

        "classical_metrics": metrics(
            observed,
            classical_predictions
        ),

        "hybrid_metrics": metrics(
            observed,
            hybrid_predictions
        ),

        "persistence_metrics": metrics(
            observed,
            persistence_predictions
        ),

        "normalization_ranges": ranges

    }