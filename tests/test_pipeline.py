"""
NeuroQ-Flood — Automated Pipeline Tests
Week 10

Tests:
1. Homeostasis
2. Persistent memory
3. Quantum baseline
4. Actual elapsed time
5. Training normalization
6. Forecaster training
7. Forecast accuracy metrics
8. Historical replay
9. Discharge trends
10. Missing discharge trends
11. Quantum feature comparison
"""

import csv
import tempfile
import unittest

from datetime import datetime, timedelta, timezone
from pathlib import Path

from neuroq.memory import (
    clamp_weights,
    save_weights,
    load_weights
)

from neuroq.quantum_model import quantum_score

from neuroq.preprocessing import (
    calculate_rise,
    fit_ranges,
    prepare
)

from neuroq.forecasting import (
    DischargeForecaster,
    calculate_discharge_trends,
    extract_features
)

from evaluation.accuracy_metrics import metrics

from evaluation.historical_replay import replay


class PipelineTests(unittest.TestCase):

    def setUp(self):

        self.weights = {
            "gage_weight": 1.0,
            "discharge_weight": 1.0,
            "change_weight": 1.0
        }

    # --------------------------------------------------
    # TEST 1 — HOMEOSTASIS
    # --------------------------------------------------

    def test_homeostasis(self):

        requested = {
            "gage_weight": 2.0,
            "discharge_weight": 0.2,
            "change_weight": 1.25
        }

        expected = {
            "gage_weight": 1.5,
            "discharge_weight": 0.5,
            "change_weight": 1.25
        }

        self.assertEqual(
            clamp_weights(requested),
            expected
        )

    # --------------------------------------------------
    # TEST 2 — PERSISTENT MEMORY
    # --------------------------------------------------

    def test_memory_roundtrip(self):

        with tempfile.TemporaryDirectory() as directory:

            path = Path(directory) / "weights.json"

            weights = {
                "gage_weight": 1.1,
                "discharge_weight": 0.9,
                "change_weight": 1.25
            }

            save_weights(path, weights)

            restored = load_weights(path)

            self.assertEqual(
                restored,
                weights
            )

    # --------------------------------------------------
    # TEST 3 — QUANTUM BASELINE
    # --------------------------------------------------

    def test_quantum_baseline(self):

        inputs = {
            "gage_height": 0.0,
            "discharge": 0.0,
            "water_change": 0.0
        }

        score, angles = quantum_score(
            inputs,
            self.weights
        )

        self.assertAlmostEqual(
            score,
            0.0
        )

        self.assertEqual(
            len(angles),
            3
        )

    # --------------------------------------------------
    # TEST 4 — ACTUAL ELAPSED TIME
    # --------------------------------------------------

    def test_actual_elapsed_time(self):

        start = datetime(
            2024, 5, 2,
            12, 0,
            tzinfo=timezone.utc
        )

        previous = {
            "timestamp": start,
            "gage_height_ft": 2.0
        }

        current = {
            "timestamp": start + timedelta(minutes=30),
            "gage_height_ft": 3.0
        }

        rise = calculate_rise(
            current,
            previous
        )

        self.assertAlmostEqual(
            rise,
            2.0
        )

    # --------------------------------------------------
    # TEST 5 — TRAINING NORMALIZATION
    # --------------------------------------------------

    def test_training_normalization(self):

        start = datetime(
            2024, 5, 2,
            tzinfo=timezone.utc
        )

        rows = [
            {
                "timestamp": start,
                "gage_height_ft": 2.0,
                "discharge_cfs": 100.0
            },
            {
                "timestamp": start + timedelta(minutes=15),
                "gage_height_ft": 4.0,
                "discharge_cfs": 200.0
            }
        ]

        ranges = fit_ranges(rows)

        self.assertEqual(
            ranges["discharge_cfs"][1],
            200.0
        )

        inputs = prepare(
            rows[1],
            rows[0],
            ranges
        )

        self.assertAlmostEqual(
            inputs["discharge"],
            100.0
        )

        self.assertTrue(
            inputs["rise_available"]
        )

    # --------------------------------------------------
    # TEST 6 — FORECASTER TRAINING
    # --------------------------------------------------

    def test_forecaster_training(self):

        features = [
            [1.0, float(i)]
            for i in range(1, 21)
        ]

        targets = [
            float(i * 2)
            for i in range(1, 21)
        ]

        model = DischargeForecaster()

        model.fit(
            features,
            targets
        )

        prediction = model.predict(
            [1.0, 10.0]
        )

        self.assertGreater(
            prediction,
            0.0
        )

        self.assertAlmostEqual(
            prediction,
            20.0,
            delta=2.0
        )

    # --------------------------------------------------
    # TEST 7 — FORECAST ACCURACY METRICS
    # --------------------------------------------------

    def test_accuracy_metrics(self):

        observed = [
            100.0,
            200.0,
            300.0
        ]

        predicted = [
            110.0,
            190.0,
            310.0
        ]

        result = metrics(
            observed,
            predicted
        )

        self.assertEqual(
            result["count"],
            3
        )

        self.assertAlmostEqual(
            result["MAE"],
            10.0
        )

        self.assertAlmostEqual(
            result["RMSE"],
            10.0
        )

        self.assertIsNotNone(
            result["NSE"]
        )

    # --------------------------------------------------
    # TEST 8 — HISTORICAL REPLAY
    # --------------------------------------------------

    def test_replay(self):

        start = datetime(
            2024, 5, 1,
            tzinfo=timezone.utc
        )

        rows = []

        for index in range(100):

            timestamp = (
                start
                + timedelta(minutes=15 * index)
            )

            rows.append({
                "timestamp": timestamp,
                "gage_height_ft": (
                    5.0 + 0.02 * index
                ),
                "discharge_cfs": (
                    200.0 + 3.0 * index
                )
            })

        with tempfile.TemporaryDirectory() as directory:

            output = (
                Path(directory)
                / "results.csv"
            )

            result = replay(
                rows,
                self.weights,
                output
            )

            self.assertEqual(
                result["measurements"],
                100
            )

            self.assertGreater(
                result["training_examples"],
                0
            )

            self.assertGreater(
                result["test_forecasts"],
                0
            )

            self.assertIn(
                "classical_metrics",
                result
            )

            self.assertIn(
                "hybrid_metrics",
                result
            )

            self.assertIn(
                "persistence_metrics",
                result
            )

            self.assertTrue(
                output.exists()
            )

            with output.open(newline="") as handle:

                reader = csv.DictReader(handle)

                saved_rows = list(reader)

                self.assertEqual(
                    len(saved_rows),
                    100
                )

                self.assertIn(
                    "classical_forecast_cfs",
                    reader.fieldnames
                )

                self.assertIn(
                    "hybrid_forecast_cfs",
                    reader.fieldnames
                )

                self.assertIn(
                    "trend_60min_cfs",
                    reader.fieldnames
                )

                self.assertIn(
                    "risk",
                    reader.fieldnames
                )

                self.assertIn(
                    "recommendation",
                    reader.fieldnames
                )

    # --------------------------------------------------
    # TEST 9 — DISCHARGE TRENDS
    # --------------------------------------------------

    def test_discharge_trends(self):

        start = datetime(
            2024, 5, 1,
            tzinfo=timezone.utc
        )

        history = {}

        measurements = [
            (0, 100.0),
            (30, 150.0),
            (45, 175.0),
            (60, 200.0)
        ]

        for minutes, discharge in measurements:

            timestamp = (
                start
                + timedelta(minutes=minutes)
            )

            history[timestamp] = {
                "timestamp": timestamp,
                "gage_height_ft": 5.0,
                "discharge_cfs": discharge
            }

        current = history[
            start + timedelta(minutes=60)
        ]

        trends, availability = (
            calculate_discharge_trends(
                current,
                history
            )
        )

        self.assertEqual(
            trends[15],
            25.0
        )

        self.assertEqual(
            trends[30],
            50.0
        )

        self.assertEqual(
            trends[60],
            100.0
        )

        self.assertEqual(
            availability[15],
            1.0
        )

    # --------------------------------------------------
    # TEST 10 — MISSING DISCHARGE TRENDS
    # --------------------------------------------------

    def test_missing_discharge_trend(self):

        timestamp = datetime(
            2024, 5, 1,
            tzinfo=timezone.utc
        )

        current = {
            "timestamp": timestamp,
            "gage_height_ft": 5.0,
            "discharge_cfs": 200.0
        }

        history = {
            timestamp: current
        }

        trends, availability = (
            calculate_discharge_trends(
                current,
                history
            )
        )

        self.assertEqual(
            trends[15],
            0.0
        )

        self.assertEqual(
            availability[15],
            0.0
        )

        self.assertEqual(
            availability[30],
            0.0
        )

        self.assertEqual(
            availability[60],
            0.0
        )

    # --------------------------------------------------
    # TEST 11 — QUANTUM FEATURE COMPARISON
    # --------------------------------------------------

    def test_quantum_feature_comparison(self):

        inputs = {
            "gage_height": 25.0,
            "discharge": 15.0,
            "water_change": 30.0,
            "rise_available": True
        }

        trends = {
            15: 20.0,
            30: 40.0,
            60: 80.0
        }

        availability = {
            15: 1.0,
            30: 1.0,
            60: 1.0
        }

        classical = extract_features(
            inputs,
            self.weights,
            500.0,
            trends,
            availability,
            include_quantum=False
        )

        hybrid = extract_features(
            inputs,
            self.weights,
            500.0,
            trends,
            availability,
            include_quantum=True
        )

        self.assertEqual(
            len(classical),
            12
        )

        self.assertEqual(
            len(hybrid),
            16
        )

        self.assertEqual(
            hybrid[:12],
            classical
        )


if __name__ == "__main__":
    unittest.main()