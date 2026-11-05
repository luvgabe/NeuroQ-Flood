"""
NeuroQ-Flood — Live Adaptive Learning

Evaluates completed forecasts using their original
saved regression models.

Only forecasts explicitly marked eligible for
learning are used.

Previously processed forecasts are excluded to
prevent duplicate learning.
"""

from neuroq.adaptive_learning import update_weights
from neuroq.forecasting import (
    DischargeForecaster,
    extract_features
)


def restore_model(model_state):
    """
    Reconstruct the original regression model
    without retraining its coefficients.
    """

    model = DischargeForecaster()

    model.coefficients = [
        float(value)
        for value in model_state["coefficients"]
    ]

    model.means = [
        float(value)
        for value in model_state["means"]
    ]

    model.scales = [
        float(value)
        for value in model_state["scales"]
    ]

    if not (
        len(model.coefficients)
        == len(model.means)
        == len(model.scales)
        == 16
    ):
        raise ValueError(
            "Invalid saved hybrid model dimensions."
        )

    return model


def predict_saved_forecast(record, weights):
    """
    Recalculate a completed forecast using candidate
    quantum weights and its original regression model.
    """

    model = restore_model(record["model_state"])

    # JSON converts integer dictionary keys to strings.
    trends = {
        int(key): float(value)
        for key, value in record["trends"].items()
    }

    availability = {
        int(key): float(value)
        for key, value in record["availability"].items()
    }

    features = extract_features(
        record["inputs"],
        weights,
        record["current_discharge_cfs"],
        trends=trends,
        availability=availability,
        include_quantum=True
    )

    return model.predict(features)


def build_feedback(records):
    """
    Create a feedback function compatible with
    the existing adaptive learning algorithm.
    """

    eligible = [
        record
        for record in records
        if (
            record.get("eligible_for_learning") is True
            and not record.get("used_for_learning", False)
        )
    ]

    if not eligible:
        raise ValueError(
            "No eligible unprocessed forecasts."
        )

    def feedback(candidate_weights):

        predictions = [
            predict_saved_forecast(
                record,
                candidate_weights
            )
            for record in eligible
        ]

        targets = [
            float(record["actual_discharge_cfs"])
            for record in eligible
        ]

        return predictions, targets

    return feedback


def learn_from_completed(state, weights):
    """
    Perform one adaptive update using newly completed,
    eligible forecasts.

    Marks processed forecasts so they cannot trigger
    learning again.
    """

    eligible = [
        record
        for record in state["completed_forecasts"]
        if (
            record.get("eligible_for_learning") is True
            and not record.get("used_for_learning", False)
        )
    ]

    if not eligible:
        return weights, 0

    feedback = build_feedback(eligible)

    updated_weights = update_weights(
        weights,
        feedback=feedback,
        enabled=True,
        learning_rate=0.001
    )

    for record in eligible:
        record["used_for_learning"] = True

    return updated_weights, len(eligible)