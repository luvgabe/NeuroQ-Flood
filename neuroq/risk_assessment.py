"""
NeuroQ-Flood — Hybrid Risk Assessment

Combines:
50% classical environmental score
50% quantum score

Risk thresholds:
0–24.99   LOW
25–49.99  MODERATE
50–74.99  HIGH
75–100    SEVERE

These thresholds are not yet calibrated
against verified historical flood events.
"""

from neuroq.quantum_model import quantum_score

from neuroq.mitigation import recommend


def analyze(inputs, weights):

    quantum, angles = quantum_score(
        inputs,
        weights
    )

    classical = 100.0 * (

        0.45 * min(
            inputs["gage_height"] / 30.0,
            1.0
        )

        +

        0.25 * min(
            inputs["discharge"] / 15.0,
            1.0
        )

        +

        0.30 * min(
            inputs["water_change"] / 20.0,
            1.0
        )

    )

    hybrid = (
        0.50 * classical
        +
        0.50 * quantum
    )

    if hybrid < 25:

        risk = "LOW"

    elif hybrid < 50:

        risk = "MODERATE"

    elif hybrid < 75:

        risk = "HIGH"

    else:

        risk = "SEVERE"

    return {

        "quantum_score": quantum,

        "classical_score": classical,

        "hybrid_score": hybrid,

        "risk": risk,

        "recommendation": recommend(risk),

        "angles_rad": angles

    }