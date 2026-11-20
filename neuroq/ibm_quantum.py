"""
NeuroQ-Flood — IBM Quantum Hardware Integration

Optional execution of NeuroQ-Flood's three-qubit
quantum circuit on real IBM Quantum hardware.

Hardware jobs are submitted only when explicitly
requested by the calling program.

IBM credentials are entered securely at runtime.
"""

from getpass import getpass

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2


def connect_ibm():

    print("\nIBM QUANTUM AUTHENTICATION")
    print("-" * 50)

    api_key = getpass("IBM Quantum API key: ")
    crn = getpass("IBM Quantum instance CRN: ")

    service = QiskitRuntimeService(
        channel="ibm_quantum_platform",
        token=api_key,
        instance=crn
    )

    return service


def build_quantum_circuit(angles):

    if len(angles) != 3:
        raise ValueError(
            "Exactly three rotation angles are required."
        )

    circuit = QuantumCircuit(3)

    for qubit, angle in enumerate(angles):
        circuit.ry(angle, qubit)

    circuit.cx(0, 1)
    circuit.cx(1, 2)

    circuit.measure_all()

    return circuit


def calculate_hardware_score(counts):

    total_shots = sum(counts.values())

    if total_shots <= 0:
        raise ValueError(
            "Hardware measurement counts are empty."
        )

    expected_ones = sum(
        count * bitstring.count("1") / 3
        for bitstring, count in counts.items()
    ) / total_shots

    return 100.0 * expected_ones


def run_hardware(
    service,
    angles,
    backend_name="ibm_fez",
    shots=1024
):

    if shots <= 0:
        raise ValueError(
            "Shots must be greater than zero."
        )

    backend = service.backend(backend_name)

    circuit = build_quantum_circuit(angles)

    hardware_circuit = transpile(
        circuit,
        backend=backend,
        optimization_level=1
    )

    sampler = SamplerV2(mode=backend)

    print(
        f"\nSubmitting circuit to {backend_name} "
        f"with {shots} shots..."
    )

    job = sampler.run(
        [hardware_circuit],
        shots=shots
    )

    print("IBM Quantum job ID:", job.job_id())

    result = job.result()

    counts = result[0].data.meas.get_counts()

    score = calculate_hardware_score(counts)

    return {
        "backend": backend_name,
        "job_id": job.job_id(),
        "shots": sum(counts.values()),
        "counts": counts,
        "hardware_score": score
    }