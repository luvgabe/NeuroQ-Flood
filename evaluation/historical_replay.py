"""
NeuroQ-Flood — Historical Replay
Week 10: Adaptive Quantum Learning

Evaluates four forecasting approaches:

1. Persistence baseline
2. Classical forecasting
3. Fixed-weight hybrid forecasting
4. Adaptive hybrid forecasting

The adaptive model updates quantum encoding weights
using completed historical forecasts.

A forecast becomes eligible for feedback only after
its target observation becomes available.

The regression coefficients remain fixed after
training. Only the quantum encoding weights adapt.
"""

import csv

from collections import deque
from datetime import timedelta
from pathlib import Path

from neuroq.preprocessing import (
    prepare,
    fit_ranges
)

from neuroq.risk_assessment import analyze

from neuroq.memory import clamp_weights

from neuroq.adaptive_learning import update_weights

from neuroq.forecasting import (
    DischargeForecaster,
    extract_features,
    calculate_discharge_trends,
    HORIZON_MINUTES
)

from evaluation.accuracy_metrics import metrics


ADAPTIVE_LEARNING_RATE = 0.001

ADAPTIVE_EPSILON = 0.001

ADAPTIVE_MAX_GRADIENT = 100.0

FEEDBACK_WINDOW = 12


def replay(rows, weights, destination):

    weights = clamp_weights(weights)

    adaptive_weights = weights.copy()

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
            == unique_rows[-1]["timestamp"]
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

    # --------------------------------------------------
    # TRAIN FORECASTING MODELS
    # --------------------------------------------------

    classical_training = []

    hybrid_training = []

    targets = []

    for index, current in enumerate(training_rows):

        future_time = (
            current["timestamp"] + horizon
        )

        future = lookup.get(future_time)

        if future is None:
            continue

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

    classical_model = DischargeForecaster()

    fixed_hybrid_model = DischargeForecaster()

    classical_model.fit(
        classical_training,
        targets
    )

    fixed_hybrid_model.fit(
        hybrid_training,
        targets
    )

    # The adaptive model starts with the same
    # trained regression coefficients.

    adaptive_model = fixed_hybrid_model

    # --------------------------------------------------
    # ADAPTIVE FEEDBACK MEMORY
    # --------------------------------------------------

    feedback_history = deque(
        maxlen=FEEDBACK_WINDOW
    )

    pending_forecasts = {}

    adaptive_updates = 0

    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------

    observed = []

    persistence_predictions = []

    classical_predictions = []

    fixed_hybrid_predictions = []

    adaptive_predictions = []

    columns = [

        "timestamp",
        "dataset_split",

        "gage_height_ft",
        "discharge_cfs",

        "trend_15min_cfs",
        "trend_30min_cfs",
        "trend_60min_cfs",

        "risk",
        "recommendation",

        "forecast_timestamp",
        "actual_future_discharge_cfs",

        "persistence_forecast_cfs",
        "classical_forecast_cfs",
        "fixed_hybrid_forecast_cfs",
        "adaptive_hybrid_forecast_cfs",

        "adaptive_gage_weight",
        "adaptive_discharge_weight",
        "adaptive_change_weight",

        "adaptive_updates"

    ]

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

            timestamp = current["timestamp"]

            # ------------------------------------------
            # PROCESS COMPLETED FORECASTS
            # ------------------------------------------

            completed = pending_forecasts.pop(
                timestamp,
                []
            )

            for completed_forecast in completed:

                feedback_history.append(
                    completed_forecast
                )

            if completed:

                def feedback(candidate_weights):

                    predictions = []

                    actual_values = []

                    for example in feedback_history:

                        features = extract_features(
                            example["inputs"],
                            candidate_weights,
                            example["discharge"],
                            example["trends"],
                            example["availability"],
                            include_quantum=True
                        )

                        prediction = (
                            adaptive_model.predict(
                                features
                            )
                        )

                        predictions.append(
                            prediction
                        )

                        actual_values.append(
                            example["actual"]
                        )

                    return (
                        predictions,
                        actual_values
                    )

                updated = update_weights(
                    adaptive_weights,
                    feedback=feedback,
                    enabled=True,
                    learning_rate=ADAPTIVE_LEARNING_RATE,
                    epsilon=ADAPTIVE_EPSILON,
                    max_gradient=ADAPTIVE_MAX_GRADIENT
                )

                if updated != adaptive_weights:

                    adaptive_weights = updated

                    adaptive_updates += 1

            # ------------------------------------------
            # PREPARE CURRENT MEASUREMENTS
            # ------------------------------------------

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

            risk_result = analyze(
                inputs,
                weights
            )

            # ------------------------------------------
            # CLASSICAL FORECAST
            # ------------------------------------------

            classical_features = extract_features(
                inputs,
                weights,
                current["discharge_cfs"],
                trends,
                availability,
                include_quantum=False
            )

            classical_prediction = (
                classical_model.predict(
                    classical_features
                )
            )

            # ------------------------------------------
            # FIXED HYBRID FORECAST
            # ------------------------------------------

            fixed_features = extract_features(
                inputs,
                weights,
                current["discharge_cfs"],
                trends,
                availability,
                include_quantum=True
            )

            fixed_prediction = (
                fixed_hybrid_model.predict(
                    fixed_features
                )
            )

            # ------------------------------------------
            # ADAPTIVE HYBRID FORECAST
            # ------------------------------------------

            adaptive_features = extract_features(
                inputs,
                adaptive_weights,
                current["discharge_cfs"],
                trends,
                availability,
                include_quantum=True
            )

            adaptive_prediction = (
                adaptive_model.predict(
                    adaptive_features
                )
            )

            persistence_prediction = (
                current["discharge_cfs"]
            )

            # ------------------------------------------
            # FUTURE TARGET
            # ------------------------------------------

            future_time = (
                timestamp + horizon
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

            # ------------------------------------------
            # QUEUE FORECAST FOR FUTURE FEEDBACK
            # ------------------------------------------

            if actual is not None:

                pending_forecasts.setdefault(
                    future_time,
                    []
                ).append({

                    "inputs": inputs.copy(),

                    "discharge":
                        current["discharge_cfs"],

                    "trends": trends.copy(),

                    "availability":
                        availability.copy(),

                    "actual": actual

                })

            # ------------------------------------------
            # EVALUATE TEST FORECASTS
            # ------------------------------------------

            if is_test and actual is not None:

                observed.append(actual)

                persistence_predictions.append(
                    persistence_prediction
                )

                classical_predictions.append(
                    classical_prediction
                )

                fixed_hybrid_predictions.append(
                    fixed_prediction
                )

                adaptive_predictions.append(
                    adaptive_prediction
                )

            # ------------------------------------------
            # SAVE RESULTS
            # ------------------------------------------

            writer.writerow({

                "timestamp":
                    timestamp.isoformat(),

                "dataset_split":
                    "TEST" if is_test else "TRAIN",

                "gage_height_ft":
                    current["gage_height_ft"],

                "discharge_cfs":
                    current["discharge_cfs"],

                "trend_15min_cfs":
                    trends[15],

                "trend_30min_cfs":
                    trends[30],

                "trend_60min_cfs":
                    trends[60],

                "risk":
                    risk_result["risk"],

                "recommendation":
                    risk_result["recommendation"],

                "forecast_timestamp":
                    future_time.isoformat(),

                "actual_future_discharge_cfs":
                    actual if actual is not None else "",

                "persistence_forecast_cfs":
                    persistence_prediction,

                "classical_forecast_cfs":
                    classical_prediction,

                "fixed_hybrid_forecast_cfs":
                    fixed_prediction,

                "adaptive_hybrid_forecast_cfs":
                    adaptive_prediction,

                "adaptive_gage_weight":
                    adaptive_weights["gage_weight"],

                "adaptive_discharge_weight":
                    adaptive_weights["discharge_weight"],

                "adaptive_change_weight":
                    adaptive_weights["change_weight"],

                "adaptive_updates":
                    adaptive_updates

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

        "persistence_metrics": metrics(
            observed,
            persistence_predictions
        ),

        "classical_metrics": metrics(
            observed,
            classical_predictions
        ),

        "hybrid_metrics": metrics(
            observed,
            fixed_hybrid_predictions
        ),

        "adaptive_metrics": metrics(
            observed,
            adaptive_predictions
        ),

        "adaptive_weights": adaptive_weights,

        "adaptive_updates": adaptive_updates,

        "normalization_ranges": ranges

    }