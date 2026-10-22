"""
NeuroQ-Flood — Discharge Forecasting
Week 10: Historical Trends and Quantum Comparison

Forecasts stream discharge 60 minutes ahead.

Supports two forecasting models:

1. Classical:
   Environmental measurements and discharge trends.

2. Hybrid:
   Environmental measurements, discharge trends,
   and quantum-derived features.

Both models use the same regression algorithm
and historical training/testing periods.

Automatic adaptive learning will be implemented
in a later development stage.
"""

import math

from datetime import timedelta

from neuroq.quantum_model import quantum_score


HORIZON_MINUTES = 60

TREND_MINUTES = (15, 30, 60)


def calculate_discharge_trends(current, history):

    """
    Calculate discharge changes over the previous
    15, 30, and 60 minutes.

    Uses exact historical timestamps.

    Missing measurements are represented by zero
    with separate availability indicators.

    No future observations are used.
    """

    timestamp = current["timestamp"]

    current_discharge = current["discharge_cfs"]

    trends = {}
    availability = {}

    for minutes in TREND_MINUTES:

        previous_time = timestamp - timedelta(
            minutes=minutes
        )

        previous = history.get(previous_time)

        if previous is None:

            trends[minutes] = 0.0
            availability[minutes] = 0.0

        else:

            trends[minutes] = (
                current_discharge
                - previous["discharge_cfs"]
            )

            availability[minutes] = 1.0

    return trends, availability


def extract_features(
    inputs,
    weights,
    current_discharge,
    trends=None,
    availability=None,
    include_quantum=True
):

    """
    Extract forecasting features.

    Both models use identical environmental
    and historical measurements.

    The hybrid model additionally includes
    quantum-derived features.
    """

    if trends is None:
        trends = {}

    if availability is None:
        availability = {}

    features = [

        # Intercept
        1.0,

        # Current discharge
        float(current_discharge),

        # Environmental measurements
        inputs["gage_height"],
        inputs["discharge"],
        inputs["water_change"],

        # Historical discharge trends
        trends.get(15, 0.0),
        trends.get(30, 0.0),
        trends.get(60, 0.0),

        # Trend availability indicators
        availability.get(15, 0.0),
        availability.get(30, 0.0),
        availability.get(60, 0.0),

        # Water-level rise availability
        float(inputs.get("rise_available", False))

    ]

    if include_quantum:

        quantum, angles = quantum_score(
            inputs,
            weights
        )

        features.extend([

            quantum,

            math.sin(angles[0]),
            math.sin(angles[1]),
            math.sin(angles[2])

        ])

    return features


class DischargeForecaster:

    def __init__(self, regularization=10.0):

        self.regularization = regularization

        self.coefficients = None

        self.means = None

        self.scales = None

    def _standardize(self, features):

        if len(features) != len(self.means):
            raise ValueError(
                "Incorrect number of forecasting features."
            )

        result = [1.0]

        for index in range(1, len(features)):

            result.append(
                (
                    features[index]
                    - self.means[index]
                )
                / self.scales[index]
            )

        return result

    def fit(self, feature_rows, targets):

        if not feature_rows:
            raise ValueError(
                "No training examples provided."
            )

        if len(feature_rows) != len(targets):
            raise ValueError(
                "Features and targets must match."
            )

        count = len(feature_rows[0])

        if any(
            len(row) != count
            for row in feature_rows
        ):
            raise ValueError(
                "Inconsistent feature dimensions."
            )

        self.means = [0.0] * count

        self.scales = [1.0] * count

        for column in range(1, count):

            values = [
                row[column]
                for row in feature_rows
            ]

            mean = sum(values) / len(values)

            variance = sum(
                (value - mean) ** 2
                for value in values
            ) / len(values)

            self.means[column] = mean

            self.scales[column] = max(
                math.sqrt(variance),
                1e-8
            )

        standardized = [
            self._standardize(row)
            for row in feature_rows
        ]

        matrix = [
            [0.0] * count
            for _ in range(count)
        ]

        vector = [0.0] * count

        for features, target in zip(
            standardized,
            targets
        ):

            for i in range(count):

                vector[i] += (
                    features[i] * target
                )

                for j in range(count):

                    matrix[i][j] += (
                        features[i] * features[j]
                    )

        for i in range(1, count):

            matrix[i][i] += self.regularization

        self.coefficients = solve_system(
            matrix,
            vector
        )

    def predict(self, features):

        if self.coefficients is None:
            raise RuntimeError(
                "Forecasting model has not been trained."
            )

        standardized = self._standardize(
            features
        )

        prediction = sum(
            coefficient * value
            for coefficient, value in zip(
                self.coefficients,
                standardized
            )
        )

        return max(0.0, prediction)


def solve_system(matrix, vector):

    size = len(vector)

    augmented = [
        matrix[i][:] + [vector[i]]
        for i in range(size)
    ]

    for column in range(size):

        pivot = max(
            range(column, size),
            key=lambda row: abs(
                augmented[row][column]
            )
        )

        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column]
        )

        divisor = augmented[column][column]

        if abs(divisor) < 1e-12:
            raise ValueError(
                "Forecasting matrix is singular."
            )

        for j in range(column, size + 1):

            augmented[column][j] /= divisor

        for row in range(size):

            if row == column:
                continue

            factor = augmented[row][column]

            for j in range(column, size + 1):

                augmented[row][j] -= (
                    factor * augmented[column][j]
                )

    return [
        augmented[i][-1]
        for i in range(size)
    ]