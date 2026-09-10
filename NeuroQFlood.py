"""
NeuroQ-Flood - Week 4 Starter
Bio-Inspired AI - Fall 2026

Week 4 Goal:
Add adaptive weights and persistent memory to the
original quantum flood model.

q0 = Gage Height
q1 = Stream Discharge
q2 = Water-Level Change

w0 = Gage Height Weight
w1 = Stream Discharge Weight
w2 = Water-Level Change Weight
"""

import json
import math
from pathlib import Path

from qiskit import QuantumCircuit


# ---------------------------------------------------------
# 1. PROJECT SETTINGS
# ---------------------------------------------------------

MEMORY_FILE = Path("adaptive_weights.json")

# All weights begin at 1.0.
# This means the first run behaves like our original model.

DEFAULT_WEIGHTS = {
    "gage_weight": 1.0,       # w0
    "discharge_weight": 1.0,  # w1
    "change_weight": 1.0      # w2
}

# Stability / homeostasis limits
MIN_WEIGHT = 0.5
MAX_WEIGHT = 1.5


# ---------------------------------------------------------
# 2. LOAD ADAPTIVE MEMORY
# ---------------------------------------------------------

def load_weights():

    # If no memory file exists, create one.
    if not MEMORY_FILE.exists():

        weights = DEFAULT_WEIGHTS.copy()

        save_weights(weights)

        return weights

    try:

        with open(MEMORY_FILE, "r") as file:

            weights = json.load(file)

        # Make sure all three weights exist.
        for key, default_value in DEFAULT_WEIGHTS.items():

            weights.setdefault(key, default_value)

        return weights

    except (json.JSONDecodeError, OSError):

        print("Could not read adaptive memory.")

        print("Resetting weights to default values.")

        weights = DEFAULT_WEIGHTS.copy()

        save_weights(weights)

        return weights


# ---------------------------------------------------------
# 3. SAVE ADAPTIVE MEMORY
# ---------------------------------------------------------

def save_weights(weights):

    with open(MEMORY_FILE, "w") as file:

        json.dump(weights, file, indent=4)


# ---------------------------------------------------------
# 4. KEEP WEIGHTS INSIDE SAFE RANGE
# ---------------------------------------------------------

def clamp_weight(value):

    return max(
        MIN_WEIGHT,
        min(MAX_WEIGHT, value)
    )


# ---------------------------------------------------------
# 5. NORMALIZATION
# ---------------------------------------------------------

def normalize(value, minimum, maximum):

    if maximum == minimum:

        return 0.0

    score = (
        (value - minimum)
        /
        (maximum - minimum)
    ) * 100

    return max(
        0.0,
        min(100.0, score)
    )


# ---------------------------------------------------------
# 6. CONVERT SCORE INTO QUANTUM ANGLE
# ---------------------------------------------------------

def score_to_angle(score):

    return (score / 100.0) * math.pi


# ---------------------------------------------------------
# 7. BUILD ADAPTIVE QUANTUM CIRCUIT
# ---------------------------------------------------------

def build_adaptive_circuit(
    gage_score,
    discharge_score,
    change_score,
    weights
):

    # Convert normalized environmental values
    # into rotation angles.

    theta0 = score_to_angle(gage_score)

    theta1 = score_to_angle(discharge_score)

    theta2 = score_to_angle(change_score)


    # Load adaptive weights.

    w0 = clamp_weight(
        weights["gage_weight"]
    )

    w1 = clamp_weight(
        weights["discharge_weight"]
    )

    w2 = clamp_weight(
        weights["change_weight"]
    )


    # Create 3-qubit circuit.

    circuit = QuantumCircuit(3, 3)


    # -----------------------------------------------------
    # ADAPTIVE ENCODING
    # -----------------------------------------------------

    # Original model:
    #
    # RY(theta)
    #
    # NeuroQ-Flood:
    #
    # RY(weight * theta)

    circuit.ry(
        w0 * theta0,
        0
    )

    circuit.ry(
        w1 * theta1,
        1
    )

    circuit.ry(
        w2 * theta2,
        2
    )


    # -----------------------------------------------------
    # ORIGINAL ENTANGLEMENT
    # -----------------------------------------------------

    circuit.cx(0, 1)

    circuit.cx(1, 2)


    # -----------------------------------------------------
    # MEASUREMENT
    # -----------------------------------------------------

    circuit.measure(
        [0, 1, 2],
        [0, 1, 2]
    )


    return circuit


# ---------------------------------------------------------
# 8. MAIN PROGRAM
# ---------------------------------------------------------

def main():

    print("=" * 60)

    print(
        "NEUROQ-FLOOD - WEEK 4 ADAPTIVE MODEL"
    )

    print("=" * 60)


    # Load previous memory.

    weights = load_weights()


    print("\nLoaded Adaptive Memory:")

    print(
        f"w0 - Gage Height Weight:        "
        f"{weights['gage_weight']:.2f}"
    )

    print(
        f"w1 - Discharge Weight:          "
        f"{weights['discharge_weight']:.2f}"
    )

    print(
        f"w2 - Water-Level Change Weight: "
        f"{weights['change_weight']:.2f}"
    )


    # -----------------------------------------------------
    # TEMPORARY WEEK 4 TEST VALUES
    # -----------------------------------------------------

    # These are normalized values from one of our
    # previous flood-model runs.
    #
    # For Week 4 we are using known values so we can
    # test the adaptive architecture before reconnecting
    # the live environmental-data system.

    gage_score = 18.03

    discharge_score = 4.44

    change_score = 13.04


    print(
        "\nNormalized Environmental Scores:"
    )

    print(
        f"q0 Gage Height Score:        "
        f"{gage_score:.2f}"
    )

    print(
        f"q1 Discharge Score:          "
        f"{discharge_score:.2f}"
    )

    print(
        f"q2 Water-Level Change Score: "
        f"{change_score:.2f}"
    )


    # Build adaptive circuit.

    circuit = build_adaptive_circuit(
        gage_score,
        discharge_score,
        change_score,
        weights
    )


    # Display circuit.

    print(
        "\nAdaptive Quantum Circuit:"
    )

    print(
        circuit.draw(output="text")
    )


    print(
        "\nEncoding Being Used:"
    )

    print(
        "q0 -> RY(w0 x theta0)"
    )

    print(
        "q1 -> RY(w1 x theta1)"
    )

    print(
        "q2 -> RY(w2 x theta2)"
    )


    print(
        "\nMemory File:"
    )

    print(
        MEMORY_FILE.resolve()
    )


    print(
        "\nWeek 4 Status:"
    )

    print(
        "[OK] Adaptive weights created"
    )

    print(
        "[OK] Weights persist between runs"
    )

    print(
        "[OK] Weight limits defined"
    )

    print(
        "[OK] Adaptive RY encoding created"
    )

    print(
        "[NEXT] Add automatic feedback rules"
    )

    print(
        "[NEXT] Reconnect live flood data"
    )

    print(
        "[NEXT] Run adaptive circuit on IBM Quantum"
    )


# ---------------------------------------------------------
# START PROGRAM
# ---------------------------------------------------------

if __name__ == "__main__":

    main()