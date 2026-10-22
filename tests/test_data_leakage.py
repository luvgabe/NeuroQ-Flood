"""
NeuroQ-Flood — Data Leakage Verification Tests

Verifies:
1. Adaptive weights remain within homeostasis limits.
2. Future observations do not affect earlier forecasts.
3. All forecasting models use the same test timestamps.
4. Adaptive learning produces valid forecasting metrics.
"""

import csv
import tempfile
import unittest

from datetime import datetime, timedelta, timezone
from pathlib import Path

from evaluation.historical_replay import replay


class DataLeakageTests(unittest.TestCase):

    def setUp(self):

        self.weights = {
            "gage_weight": 1.0,
            "discharge_weight": 1.0,
            "change_weight": 1.0
        }

        self.start = datetime(
            2024, 5, 1,
            tzinfo=timezone.utc
        )

    def create_rows(self, count=120):

        rows = []

        for index in range(count):

            rows.append({

                "timestamp":
                    self.start
                    + timedelta(minutes=15 * index),

                "gage_height_ft":
                    3.0 + 0.03 * index,

                "discharge_cfs":
                    150.0 + 4.0 * index

            })

        return rows

    def run_replay(self, rows):

        with tempfile.TemporaryDirectory() as directory:

            output = Path(directory) / "results.csv"

            result = replay(
                rows,
                self.weights,
                output
            )

            with output.open(newline="") as handle:

                records = list(
                    csv.DictReader(handle)
                )

            return result, records

    # --------------------------------------------
    # TEST 1 — HOMEOSTASIS
    # --------------------------------------------

    def test_adaptive_homeostasis(self):

        rows = self.create_rows()

        result, records = self.run_replay(rows)

        for record in records:

            for key in (
                "adaptive_gage_weight",
                "adaptive_discharge_weight",
                "adaptive_change_weight"
            ):

                weight = float(record[key])

                self.assertGreaterEqual(
                    weight,
                    0.5
                )

                self.assertLessEqual(
                    weight,
                    1.5
                )

    # --------------------------------------------
    # TEST 2 — NO FUTURE OBSERVATION LEAKAGE
    # --------------------------------------------

    def test_future_data_does_not_change_past(self):

        original_rows = self.create_rows()

        modified_rows = [
            row.copy()
            for row in original_rows
        ]

        # Modify observations only near the end
        # of the dataset.

        for index in range(105, 120):

            modified_rows[index][
                "discharge_cfs"
            ] += 5000.0

        _, original = self.run_replay(
            original_rows
        )

        _, modified = self.run_replay(
            modified_rows
        )

        # Compare predictions issued before the
        # changed measurements could be observed.

        for index in range(105):

            self.assertAlmostEqual(
                float(
                    original[index][
                        "adaptive_hybrid_forecast_cfs"
                    ]
                ),
                float(
                    modified[index][
                        "adaptive_hybrid_forecast_cfs"
                    ]
                ),
                places=6
            )

    # --------------------------------------------
    # TEST 3 — SAME EVALUATION TIMESTAMPS
    # --------------------------------------------

    def test_matching_forecast_timestamps(self):

        rows = self.create_rows()

        result, records = self.run_replay(rows)

        evaluated = [
            row
            for row in records
            if (
                row["dataset_split"] == "TEST"
                and row["actual_future_discharge_cfs"]
            )
        ]

        for row in evaluated:

            self.assertNotEqual(
                row["persistence_forecast_cfs"],
                ""
            )

            self.assertNotEqual(
                row["classical_forecast_cfs"],
                ""
            )

            self.assertNotEqual(
                row["fixed_hybrid_forecast_cfs"],
                ""
            )

            self.assertNotEqual(
                row["adaptive_hybrid_forecast_cfs"],
                ""
            )

        self.assertEqual(
            len(evaluated),
            result["test_forecasts"]
        )

    # --------------------------------------------
    # TEST 4 — VALID ADAPTIVE METRICS
    # --------------------------------------------

    def test_adaptive_metrics(self):

        rows = self.create_rows()

        result, _ = self.run_replay(rows)

        adaptive = result["adaptive_metrics"]

        self.assertGreater(
            adaptive["count"],
            0
        )

        self.assertGreaterEqual(
            adaptive["MAE"],
            0
        )

        self.assertGreaterEqual(
            adaptive["RMSE"],
            0
        )


if __name__ == "__main__":
    unittest.main()