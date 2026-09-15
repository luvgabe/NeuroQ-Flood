# =========================================================
# NeuroQ-Flood
# Bio-Inspired AI - Fall 2026
# Gabriel Granados & Alberto Gonzalez
#
# WEEK 5:
# Adaptive Quantum Encoding
# =========================================================

import json
import math
from pathlib import Path

from qiskit import QuantumCircuit


# =========================================================
# PROJECT SETTINGS
# =========================================================

MEMORY_FILE = Path("adaptive_weights.json")

DEFAULT_WEIGHTS = {
    "gage_weight": 1.0,       # w0
    "discharge_weight": 1.0,  # w1
    "change_weight": 1.0      # w2
}

# Homeostasis / stability limits
MIN_WEIGHT = 0.5
MAX_WEIGHT = 1.5


# =========================================================
# LOAD ADAPTIVE MEMORY
# =========================================================

def load_weights():

    if not MEMORY_FILE.exists():

        weights = DEFAULT_WEIGHTS.copy()
        save_weights(weights)

        return weights

    try:

        with open(MEMORY_FILE, "r") as file:
            weights = json.load(file)

        for key, default_value in DEFAULT_WEIGHTS.items():
            weights.setdefault(key, default_value)

        return weights

    except (json.JSONDecodeError, OSError):

        print("Could not read adaptive memory.")
        print("Resetting weights to default values.")

        weights = DEFAULT_WEIGHTS.copy()
        save_weights(weights)

        return weights


# =========================================================
# SAVE ADAPTIVE MEMORY
# =========================================================

def save_weights(weights):

    with open(MEMORY_FILE, "w") as file:

        json.dump(
            weights,
            file,
            indent=4
        )


# =========================================================
# HOMEOSTASIS / WEIGHT STABILITY
# =========================================================

def clamp_weight(value):

    return max(
        MIN_WEIGHT,
        min(MAX_WEIGHT, value)
    )


# =========================================================
# NORMALIZATION
# =========================================================

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


# =========================================================
# CONVERT SCORE TO QUANTUM ANGLE
# =========================================================

def score_to_angle(score):

    return (score / 100.0) * math.pi


# =========================================================
# CALCULATE ADAPTIVE ANGLES
# =========================================================

def calculate_adaptive_angles(
    gage_score,
    discharge_score,
    change_score,
    weights
):

    # Original quantum angles
    theta0 = score_to_angle(gage_score)
    theta1 = score_to_angle(discharge_score)
    theta2 = score_to_angle(change_score)

    # Apply stability limits to weights
    w0 = clamp_weight(weights["gage_weight"])
    w1 = clamp_weight(weights["discharge_weight"])
    w2 = clamp_weight(weights["change_weight"])

    # Adaptive quantum angles
    adaptive_theta0 = w0 * theta0
    adaptive_theta1 = w1 * theta1
    adaptive_theta2 = w2 * theta2

    return {
        "theta0": theta0,
        "theta1": theta1,
        "theta2": theta2,

        "w0": w0,
        "w1": w1,
        "w2": w2,

        "adaptive_theta0": adaptive_theta0,
        "adaptive_theta1": adaptive_theta1,
        "adaptive_theta2": adaptive_theta2
    }


# =========================================================
# BUILD ADAPTIVE QUANTUM CIRCUIT
# =========================================================

def build_adaptive_circuit(
    gage_score,
    discharge_score,
    change_score,
    weights
):

    values = calculate_adaptive_angles(
        gage_score,
        discharge_score,
        change_score,
        weights
    )

    circuit = QuantumCircuit(3, 3)

    # -----------------------------------------------------
    # Adaptive RY encoding
    #
    # q0 -> RY(w0 * theta0)
    # q1 -> RY(w1 * theta1)
    # q2 -> RY(w2 * theta2)
    # -----------------------------------------------------

    circuit.ry(
        values["adaptive_theta0"],
        0
    )

    circuit.ry(
        values["adaptive_theta1"],
        1
    )

    circuit.ry(
        values["adaptive_theta2"],
        2
    )

    # Entanglement
    circuit.cx(0, 1)
    circuit.cx(1, 2)

    # Measurement
    circuit.measure(
        [0, 1, 2],
        [0, 1, 2]
    )

    return circuit, values


# =========================================================
# DISPLAY ENCODING TEST
# =========================================================

def display_encoding_test(
    name,
    weights,
    gage_score,
    discharge_score,
    change_score
):

    print("\n")
    print("=" * 65)
    print(name)
    print("=" * 65)

    circuit, values = build_adaptive_circuit(
        gage_score,
        discharge_score,
        change_score,
        weights
    )

    # -----------------------------------------------------
    # Display weights
    # -----------------------------------------------------

    print("\nWEIGHTS")

    print(
        f"w0 - Gage Height:        "
        f"{values['w0']:.2f}"
    )

    print(
        f"w1 - Stream Discharge:   "
        f"{values['w1']:.2f}"
    )

    print(
        f"w2 - Water-Level Change: "
        f"{values['w2']:.2f}"
    )

    # -----------------------------------------------------
    # q0
    # -----------------------------------------------------

    print("\nQUANTUM ENCODING")

    print("\nq0 - Gage Height")

    print(
        f"Original angle: "
        f"{values['theta0']:.4f} radians"
    )

    print(
        f"Adaptive angle: "
        f"{values['adaptive_theta0']:.4f} radians"
    )

    # -----------------------------------------------------
    # q1
    # -----------------------------------------------------

    print("\nq1 - Stream Discharge")

    print(
        f"Original angle: "
        f"{values['theta1']:.4f} radians"
    )

    print(
        f"Adaptive angle: "
        f"{values['adaptive_theta1']:.4f} radians"
    )

    # -----------------------------------------------------
    # q2
    # -----------------------------------------------------

    print("\nq2 - Water-Level Change")

    print(
        f"Original angle: "
        f"{values['theta2']:.4f} radians"
    )

    print(
        f"Adaptive angle: "
        f"{values['adaptive_theta2']:.4f} radians"
    )

    # -----------------------------------------------------
    # Display quantum circuit
    # -----------------------------------------------------

    print("\nQUANTUM CIRCUIT")

    print(
        circuit.draw(
            output="text"
        )
    )


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    print("=" * 65)

    print("NEUROQ-FLOOD")
    print("Week 5 - Adaptive Quantum Encoding")

    print("=" * 65)

    # -----------------------------------------------------
    # Load persistent memory
    # -----------------------------------------------------

    saved_weights = load_weights()

    print("\nSAVED ADAPTIVE MEMORY")

    print(
        f"w0 = "
        f"{saved_weights['gage_weight']:.2f}"
    )

    print(
        f"w1 = "
        f"{saved_weights['discharge_weight']:.2f}"
    )

    print(
        f"w2 = "
        f"{saved_weights['change_weight']:.2f}"
    )


    # =====================================================
    # WEEK 5 CONTROLLED TEST DATA
    # =====================================================
    #
    # We keep the environmental measurements constant
    # during all three tests.
    #
    # This allows us to prove that changes in the quantum
    # circuit come from the weights instead of changes
    # in environmental conditions.
    # =====================================================

    gage_score = 18.03
    discharge_score = 4.44
    change_score = 13.04

    print("\nCONTROLLED ENVIRONMENTAL INPUT")

    print(
        f"q0 - Gage Height:        "
        f"{gage_score:.2f}"
    )

    print(
        f"q1 - Stream Discharge:   "
        f"{discharge_score:.2f}"
    )

    print(
        f"q2 - Water-Level Change: "
        f"{change_score:.2f}"
    )


    # =====================================================
    # TEST 1 - BASELINE
    # =====================================================
    #
    # Every weight = 1.0
    #
    # Therefore:
    #
    # RY(1.0 * theta) = RY(theta)
    #
    # This represents the original model behavior.
    # =====================================================

    baseline_weights = {

        "gage_weight": 1.0,

        "discharge_weight": 1.0,

        "change_weight": 1.0
    }

    display_encoding_test(
        "TEST 1 - BASELINE ENCODING",
        baseline_weights,
        gage_score,
        discharge_score,
        change_score
    )


    # =====================================================
    # TEST 2 - ADAPTIVE ENCODING
    # =====================================================
    #
    # We manually simulate an adapted state.
    #
    # w0 > 1 = stronger gage-height influence
    # w1 < 1 = weaker discharge influence
    # w2 > 1 = stronger water-change influence
    #
    # Week 6 will eventually determine changes like
    # these automatically.
    # =====================================================

    adaptive_test_weights = {

        "gage_weight": 1.10,

        "discharge_weight": 0.90,

        "change_weight": 1.25
    }

    display_encoding_test(
        "TEST 2 - ADAPTIVE ENCODING",
        adaptive_test_weights,
        gage_score,
        discharge_score,
        change_score
    )


    # =====================================================
    # TEST 3 - HOMEOSTASIS
    # =====================================================
    #
    # Deliberately give the system unsafe weights.
    #
    # Requested:
    #
    # w0 = 1.80
    # w1 = 0.20
    # w2 = 1.25
    #
    # Expected after clamp_weight():
    #
    # w0 = 1.50
    # w1 = 0.50
    # w2 = 1.25
    #
    # This proves our stability system works.
    # =====================================================

    unstable_weights = {

        "gage_weight": 1.80,

        "discharge_weight": 0.20,

        "change_weight": 1.25
    }

    display_encoding_test(
        "TEST 3 - HOMEOSTASIS LIMIT TEST",
        unstable_weights,
        gage_score,
        discharge_score,
        change_score
    )


    # =====================================================
    # WEEK 5 STATUS
    # =====================================================

    print("\n")
    print("=" * 65)

    print("WEEK 5 STATUS")

    print("=" * 65)

    print(
        "[OK] Environmental inputs remain q0, q1, q2"
    )

    print(
        "[OK] Adaptive parameters remain w0, w1, w2"
    )

    print(
        "[OK] Weights modify quantum rotation angles"
    )

    print(
        "[OK] RY(w x theta) encoding implemented"
    )

    print(
        "[OK] Homeostasis limits tested"
    )

    print(
        "[OK] Persistent memory retained"
    )

    print("\nNEXT: WEEK 6")

    print(
        "Replace manual weight changes with "
        "automatic feedback."
    )


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":

    main()