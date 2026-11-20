"""
NeuroQ-Flood — IBM Quantum Comparison

Compares the existing local quantum statevector
simulation against execution on IBM Quantum hardware.

Hardware execution requires explicit confirmation.
"""

from pathlib import Path

from neuroq.data_source import get_recent_usgs
from neuroq.preprocessing import fit_ranges, prepare
from neuroq.quantum_model import quantum_score
from neuroq.memory import DEFAULT_WEIGHTS, clamp_weights
from neuroq.live_memory import load_live_state

from neuroq.ibm_quantum import (
    connect_ibm,
    run_hardware
)


ROOT = Path(__file__).resolve().parent.parent


def run_ibm_comparison(
    backend_name="ibm_fez",
    shots=1024
):

    if shots <= 0:
        raise ValueError("Shots must be positive.")

    print("\n" + "=" * 60)
    print("NEUROQ-FLOOD — IBM QUANTUM COMPARISON")
    print("=" * 60)

    print("\nRetrieving recent USGS measurements...")

    rows = get_recent_usgs(days=14)

    rows = sorted(
        {row["timestamp"]: row for row in rows}.values(),
        key=lambda row: row["timestamp"]
    )

    if len(rows) < 2:
        raise RuntimeError(
            "At least two USGS observations are required."
        )

    training_rows = rows[:-1]

    ranges = fit_ranges(training_rows)

    inputs = prepare(
        rows[-1],
        rows[-2],
        ranges
    )

    state_path = ROOT / "data" / "live" / "live_state.json"

    state = load_live_state(state_path)

    if state["adaptive_weights"] is not None:
        weights = clamp_weights(
            state["adaptive_weights"]
        )
    else:
        weights = clamp_weights(
            dict.fromkeys(DEFAULT_WEIGHTS, 1.0)
        )

    local_score, angles = quantum_score(
        inputs,
        weights
    )

    print("\nStation: 08074000")
    print("Observation:", rows[-1]["timestamp"])
    print("Gage height:", rows[-1]["gage_height_ft"], "ft")
    print("Discharge:", rows[-1]["discharge_cfs"], "cfs")

    print("\nNormalized inputs:", inputs)
    print("Quantum weights:", weights)

    print("\nLOCAL QUANTUM SIMULATION")
    print("-" * 60)

    print(f"Local quantum score: {local_score:.4f}")
    print("Rotation angles:", angles)

    print("\nIBM HARDWARE CONFIGURATION")
    print("-" * 60)

    print("Backend:", backend_name)
    print("Shots:", shots)

    print(
        "\nWARNING: Submitting a hardware job "
        "will consume IBM Quantum Runtime Units."
    )

    confirmation = input(
        "\nSubmit this experiment to IBM hardware? "
        "(yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("\nHardware submission cancelled.")
        return None

    service = connect_ibm()

    result = run_hardware(
        service,
        angles,
        backend_name=backend_name,
        shots=shots
    )

    hardware_score = result["hardware_score"]

    difference = abs(
        local_score - hardware_score
    )

    print("\n" + "=" * 60)
    print("IBM QUANTUM COMPARISON RESULTS")
    print("=" * 60)

    print("Backend:", result["backend"])
    print("Job ID:", result["job_id"])
    print("Shots:", result["shots"])

    print("\nMeasurement counts:")

    for bitstring, count in sorted(
        result["counts"].items()
    ):
        print(f"  {bitstring}: {count}")

    print(f"\nLocal quantum score: {local_score:.4f}")
    print(f"IBM hardware score: {hardware_score:.4f}")
    print(f"Absolute difference: {difference:.4f}")

    print(
        "\nNOTE: Differences can result from "
        "measurement sampling and hardware noise."
    )

    print("=" * 60)

    return {
        "observation_time": rows[-1]["timestamp"],
        "inputs": inputs,
        "weights": weights,
        "angles": angles,
        "local_score": local_score,
        "hardware_score": hardware_score,
        "absolute_difference": difference,
        "hardware_result": result
    }