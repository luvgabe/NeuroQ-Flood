"""
NeuroQ-Flood — IBM Quantum Integration Tests

Tests circuit construction, measurement processing,
and hardware execution using mocked IBM services.

No real IBM Quantum jobs are submitted.
No IBM Runtime Units are consumed.
"""

import math
from unittest.mock import MagicMock, patch

import pytest

from neuroq.ibm_quantum import (
    build_quantum_circuit,
    calculate_hardware_score,
    run_hardware
)

from neuroq.quantum_model import quantum_score

from qiskit.quantum_info import Statevector


# --------------------------------------------------
# CIRCUIT CONSTRUCTION
# --------------------------------------------------

def test_circuit_has_three_qubits():

    circuit = build_quantum_circuit(
        [0.5, 0.8, 0.3]
    )

    assert circuit.num_qubits == 3


def test_circuit_has_expected_gates():

    circuit = build_quantum_circuit(
        [0.5, 0.8, 0.3]
    )

    operations = circuit.count_ops()

    assert operations["ry"] == 3
    assert operations["cx"] == 2
    assert operations["measure"] == 3


def test_circuit_has_correct_gate_order():

    circuit = build_quantum_circuit(
        [0.5, 0.8, 0.3]
    )

    gates = [
        instruction.operation.name
        for instruction in circuit.data
    ]

    assert gates[:5] == [
        "ry",
        "ry",
        "ry",
        "cx",
        "cx"
    ]


def test_circuit_rejects_invalid_angle_count():

    with pytest.raises(ValueError):

        build_quantum_circuit(
            [0.5, 0.8]
        )


# --------------------------------------------------
# HARDWARE SCORE CALCULATIONS
# --------------------------------------------------

def test_hardware_score_all_zeros():

    counts = {
        "000": 1024
    }

    assert calculate_hardware_score(counts) == 0.0


def test_hardware_score_all_ones():

    counts = {
        "111": 1024
    }

    assert calculate_hardware_score(counts) == 100.0


def test_hardware_score_equal_distribution():

    counts = {
        "000": 512,
        "111": 512
    }

    assert calculate_hardware_score(counts) == 50.0


def test_hardware_score_mixed_distribution():

    counts = {
        "000": 256,
        "001": 256,
        "011": 256,
        "111": 256
    }

    expected = 50.0

    assert calculate_hardware_score(
        counts
    ) == pytest.approx(expected)


def test_hardware_score_rejects_empty_counts():

    with pytest.raises(ValueError):

        calculate_hardware_score({})


# --------------------------------------------------
# LOCAL SIMULATOR VS QISKIT
# --------------------------------------------------

def test_local_simulator_matches_qiskit():

    inputs = {
        "gage_height": 40.0,
        "discharge": 60.0,
        "water_change": 20.0
    }

    weights = {
        "gage_weight": 1.0,
        "discharge_weight": 1.0,
        "change_weight": 1.0
    }

    local_score, angles = quantum_score(
        inputs,
        weights
    )

    circuit = build_quantum_circuit(
        angles
    )

    # Remove measurements for statevector simulation.
    circuit = circuit.remove_final_measurements(
        inplace=False
    )

    state = Statevector.from_instruction(
        circuit
    )

    expected_ones = sum(
        probability * bitstring.count("1") / 3
        for bitstring, probability
        in state.probabilities_dict().items()
    )

    qiskit_score = 100.0 * expected_ones

    assert local_score == pytest.approx(
        qiskit_score,
        abs=1e-10
    )


# --------------------------------------------------
# MOCKED IBM HARDWARE EXECUTION
# --------------------------------------------------

@patch("neuroq.ibm_quantum.SamplerV2")
@patch("neuroq.ibm_quantum.transpile")
def test_hardware_execution_mocked(
    mock_transpile,
    mock_sampler
):

    service = MagicMock()

    backend = MagicMock()

    service.backend.return_value = backend

    mock_transpile.side_effect = (
        lambda circuit, **kwargs: circuit
    )

    job = MagicMock()

    job.job_id.return_value = "mock-job-123"

    result = MagicMock()

    result.__getitem__.return_value.data.meas.get_counts.return_value = {
        "000": 512,
        "111": 512
    }

    job.result.return_value = result

    sampler_instance = mock_sampler.return_value

    sampler_instance.run.return_value = job

    output = run_hardware(
        service,
        [0.5, 0.8, 0.3],
        backend_name="ibm_fez",
        shots=1024
    )

    assert output["backend"] == "ibm_fez"

    assert output["job_id"] == "mock-job-123"

    assert output["shots"] == 1024

    assert output["hardware_score"] == 50.0

    service.backend.assert_called_once_with(
        "ibm_fez"
    )

    sampler_instance.run.assert_called_once()


def test_hardware_rejects_invalid_shots():

    service = MagicMock()

    with pytest.raises(ValueError):

        run_hardware(
            service,
            [0.5, 0.8, 0.3],
            shots=0
        )

    service.backend.assert_not_called()