"""
NeuroQ-Flood — Environmental Preprocessing

Normalizes environmental measurements and
calculates water-level change using actual time.

Normalization parameters can be fitted using
historical training measurements.

The default ranges are provisional and are
retained for compatibility with existing code.
"""

from math import isfinite


DEFAULT_RANGES = {

    "gage_height_ft": (0.0, 40.0),

    "discharge_cfs": (0.0, 100000.0),

    "rise_ft_per_hour": (0.0, 5.0)

}

RANGES = DEFAULT_RANGES


def scale(value, low, high):

    if not (
        isfinite(value)
        and isfinite(low)
        and isfinite(high)
    ):
        raise ValueError(
            "Normalization values must be finite."
        )

    if high <= low:
        raise ValueError(
            "Normalization maximum must exceed minimum."
        )

    normalized = (
        100.0
        * (value - low)
        / (high - low)
    )

    return max(
        0.0,
        min(100.0, normalized)
    )


def calculate_rise(current, previous=None):

    if previous is None:
        return None

    elapsed = (
        current["timestamp"]
        - previous["timestamp"]
    ).total_seconds() / 3600.0

    if not 0 < elapsed <= 2.0:
        return None

    return (
        current["gage_height_ft"]
        - previous["gage_height_ft"]
    ) / elapsed


def fit_ranges(rows):

    if not rows:
        raise ValueError(
            "Cannot fit normalization without data."
        )

    gage_values = [
        row["gage_height_ft"]
        for row in rows
    ]

    discharge_values = [
        row["discharge_cfs"]
        for row in rows
    ]

    rise_values = []

    for index in range(1, len(rows)):

        rise = calculate_rise(
            rows[index],
            rows[index - 1]
        )

        if rise is not None:
            rise_values.append(
                max(0.0, rise)
            )

    def upper_limit(values):

        return max(
            max(values),
            1e-6
        )

    return {

        "gage_height_ft": (
            0.0,
            upper_limit(gage_values)
        ),

        "discharge_cfs": (
            0.0,
            upper_limit(discharge_values)
        ),

        "rise_ft_per_hour": (
            0.0,
            upper_limit(rise_values)
            if rise_values else 5.0
        )

    }


def prepare(
    current,
    previous=None,
    ranges=None
):

    if ranges is None:
        ranges = DEFAULT_RANGES

    rise = calculate_rise(
        current,
        previous
    )

    return {

        "gage_height": scale(
            current["gage_height_ft"],
            *ranges["gage_height_ft"]
        ),

        "discharge": scale(
            current["discharge_cfs"],
            *ranges["discharge_cfs"]
        ),

        "water_change": scale(
            max(0.0, rise)
            if rise is not None else 0.0,
            *ranges["rise_ft_per_hour"]
        ),

        "rise_ft_per_hour": rise,

        "rise_available": (
            rise is not None
        )

    }