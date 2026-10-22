"""
NeuroQ-Flood — Adaptive Quantum Learning

Implements feedback-driven optimization of quantum
encoding weights using observed forecasting errors.

Features:
- Finite-difference gradient estimation
- Homeostasis-constrained weight updates
- Learning-rate control
- Optional gradient clipping
- Rejection of updates that increase training loss

IMPORTANT:
Feedback must contain only observations whose
forecast targets are already available.

Evaluation data must not be used to select weights.
"""

import math

from neuroq.memory import (
    DEFAULT_WEIGHTS,
    clamp_weights
)


def mean_squared_error(predictions, targets):
    """Calculate mean squared forecasting error."""

    if not predictions or len(predictions) != len(targets):
        raise ValueError(
            "Predictions and targets must be nonempty "
            "and have equal lengths."
        )

    return sum(
        (prediction - target) ** 2
        for prediction, target in zip(predictions, targets)
    ) / len(targets)


def calculate_loss(weights, feedback):
    """
    Evaluate forecasting error for candidate weights.

    feedback must be a callable accepting a weight
    dictionary and returning (predictions, targets).

    The callable must evaluate only permitted
    training observations.
    """

    predictions, targets = feedback(weights)

    return mean_squared_error(predictions, targets)


def update_weights(
    weights,
    feedback=None,
    enabled=False,
    learning_rate=0.01,
    epsilon=0.001,
    max_gradient=100.0
):
    """
    Perform one adaptive quantum-weight update.

    Uses central finite differences to estimate
    how changing each encoding weight affects
    forecasting loss.

    Accepts the update only if it improves loss.

    This function does not retrain the forecasting
    regression coefficients. The feedback callable
    determines how candidate weights are evaluated.
    """

    weights = clamp_weights(weights)

    if not enabled:
        return weights

    if feedback is None or not callable(feedback):
        raise ValueError(
            "Adaptive learning requires a feedback "
            "function."
        )

    if learning_rate <= 0:
        raise ValueError(
            "Learning rate must be positive."
        )

    if epsilon <= 0:
        raise ValueError(
            "Epsilon must be positive."
        )

    if max_gradient <= 0:
        raise ValueError(
            "Maximum gradient must be positive."
        )

    baseline_loss = calculate_loss(
        weights,
        feedback
    )

    gradients = {}

    for key in DEFAULT_WEIGHTS:

        plus = weights.copy()
        minus = weights.copy()

        plus[key] = min(
            1.5,
            weights[key] + epsilon
        )

        minus[key] = max(
            0.5,
            weights[key] - epsilon
        )

        if plus[key] == minus[key]:
            gradients[key] = 0.0
            continue

        loss_plus = calculate_loss(
            plus,
            feedback
        )

        loss_minus = calculate_loss(
            minus,
            feedback
        )

        gradient = (
            loss_plus - loss_minus
        ) / (
            plus[key] - minus[key]
        )

        gradients[key] = max(
            -max_gradient,
            min(max_gradient, gradient)
        )

    candidate = {}

    for key in DEFAULT_WEIGHTS:

        candidate[key] = (
            weights[key]
            - learning_rate * gradients[key]
        )

    candidate = clamp_weights(candidate)

    candidate_loss = calculate_loss(
        candidate,
        feedback
    )

    if (
        math.isfinite(candidate_loss)
        and candidate_loss < baseline_loss
    ):
        return candidate

    return weights