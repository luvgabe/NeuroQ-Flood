"""
NeuroQ-Flood — Adaptive Learning

Current checkpoint:
- Weight validation
- Homeostasis integration

Next checkpoint:
- Automatic feedback-based learning
- Prediction-error-driven updates
"""

from neuroq.memory import clamp_weights


def update_weights(
    weights,
    feedback=None,
    enabled=False
):

    if enabled:

        raise NotImplementedError(
            "Automatic learning will be implemented "
            "in the next checkpoint."
        )

    return clamp_weights(weights)