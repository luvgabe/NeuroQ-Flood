"""
NeuroQ-Flood — Persistent Live Forecast Memory

Stores live forecasting state between executions.
"""

import json

from pathlib import Path
from datetime import datetime, timezone


def load_live_state(path):
    path = Path(path)

    if not path.exists():
        return {
            "pending_forecasts": [],
            "completed_forecasts": [],
            "adaptive_weights": None
        }

    with path.open("r") as handle:
        state = json.load(handle)

    return {
        "pending_forecasts": state.get(
            "pending_forecasts", []
        ),
        "completed_forecasts": state.get(
            "completed_forecasts", []
        ),
        "adaptive_weights": state.get(
            "adaptive_weights"
        )
    }


def save_live_state(path, state):
    """Save live forecasting state atomically."""

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temporary = path.with_suffix(
        path.suffix + ".tmp"
    )

    with temporary.open("w") as handle:
        json.dump(
            state,
            handle,
            indent=2
        )

    temporary.replace(path)

    from datetime import datetime, timezone


def complete_forecasts(state, observations):
    """
    Match pending forecasts with actual USGS
    observations at their target timestamps.

    Only exact timestamp matches are accepted.
    """

    lookup = {
        row["timestamp"].astimezone(timezone.utc): row
        for row in observations
    }

    pending = []
    newly_completed = []

    for forecast in state["pending_forecasts"]:

        target = datetime.fromisoformat(
            forecast["target_timestamp"].replace(
                "Z", "+00:00"
            )
        ).astimezone(timezone.utc)

        actual_row = lookup.get(target)

        if actual_row is None:
            pending.append(forecast)
            continue

        actual = actual_row["discharge_cfs"]

        completed = forecast.copy()

        issued_at_text = forecast.get("issued_at")

        if issued_at_text is None:
            completed["eligible_for_learning"] = False
        else:
            issued_at = datetime.fromisoformat(
                issued_at_text.replace("Z", "+00:00")
            ).astimezone(timezone.utc)

            completed["eligible_for_learning"] = (
                issued_at < target
            )

        completed["actual_discharge_cfs"] = actual

        completed["error_cfs"] = (
            forecast["prediction_cfs"] - actual
        )

        completed["absolute_error_cfs"] = abs(
            completed["error_cfs"]
        )

        newly_completed.append(completed)

    state["pending_forecasts"] = pending

    state["completed_forecasts"].extend(
        newly_completed
    )

    return newly_completed