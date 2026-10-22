"""
NeuroQ-Flood — Persistent Adaptive Memory

Stores adaptive weights between executions.

Homeostasis:
0.5 <= weight <= 1.5
"""

import json

from pathlib import Path


DEFAULT_WEIGHTS = {

    "gage_weight": 1.0,

    "discharge_weight": 1.0,

    "change_weight": 1.0

}


def clamp_weights(weights):

    return {

        key: max(
            0.5,
            min(
                1.5,
                float(weights[key])
            )
        )

        for key in DEFAULT_WEIGHTS

    }


def load_weights(path):

    path = Path(path)

    if not path.exists():
        return DEFAULT_WEIGHTS.copy()

    data = json.loads(
        path.read_text()
    )

    return clamp_weights(data)


def save_weights(path, weights):

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temporary = path.with_suffix(
        path.suffix + ".tmp"
    )

    temporary.write_text(
        json.dumps(
            clamp_weights(weights),
            indent=2
        ) + "\n"
    )

    temporary.replace(path)