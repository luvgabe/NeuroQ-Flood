"""
NeuroQ-Flood — Quantum Model

Exact local statevector simulation.

Three qubits:
q0 = Gage height
q1 = Discharge
q2 = Water-level change

Circuit:
RY rotations followed by CX(0,1) and CX(1,2).

No IBM Quantum hardware is required.
"""

import math


def quantum_score(inputs, weights):

    signals = (

        inputs["gage_height"],

        inputs["discharge"],

        inputs["water_change"]

    )

    weight_values = (

        weights["gage_weight"],

        weights["discharge_weight"],

        weights["change_weight"]

    )

    angles = [

        math.pi * signal * weight / 100.0

        for signal, weight
        in zip(signals, weight_values)

    ]

    # Initialize |000>

    state = [0.0] * 8

    state[0] = 1.0

    # Apply RY rotations

    for qubit, angle in enumerate(angles):

        c = math.cos(angle / 2)

        s = math.sin(angle / 2)

        bit = 1 << qubit

        for i in range(8):

            if i & bit:
                continue

            j = i | bit

            a = state[i]
            b = state[j]

            state[i] = c * a - s * b
            state[j] = s * a + c * b

    # Apply CX entangling gates

    for control, target in (
        (0, 1),
        (1, 2)
    ):

        control_bit = 1 << control
        target_bit = 1 << target

        for i in range(8):

            if (
                i & control_bit
                and not i & target_bit
            ):

                j = i | target_bit

                state[i], state[j] = (
                    state[j],
                    state[i]
                )

    # Expected fraction of measured 1 bits

    expected_ones = sum(

        (amplitude ** 2)
        * i.bit_count()
        / 3

        for i, amplitude
        in enumerate(state)

    )

    score = 100.0 * expected_ones

    return score, angles