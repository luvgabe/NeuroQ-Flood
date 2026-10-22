"""
NeuroQ-Flood — Adaptive Learning Tests

Tests automatic weight optimization and
homeostasis constraints.
"""

import unittest

from neuroq.adaptive_learning import (
    update_weights,
    mean_squared_error
)


class AdaptiveLearningTests(unittest.TestCase):

    def setUp(self):

        self.weights = {
            "gage_weight": 1.0,
            "discharge_weight": 1.0,
            "change_weight": 1.0
        }

    def test_mean_squared_error(self):

        result = mean_squared_error(
            [100.0, 200.0],
            [110.0, 190.0]
        )

        self.assertAlmostEqual(
            result,
            100.0
        )

    def test_learning_disabled(self):

        updated = update_weights(
            self.weights,
            enabled=False
        )

        self.assertEqual(
            updated,
            self.weights
        )

    def test_feedback_required(self):

        with self.assertRaises(ValueError):

            update_weights(
                self.weights,
                enabled=True
            )

    def test_adaptive_learning(self):

        def feedback(weights):

            prediction = (
                100.0
                + 100.0 * (
                    weights["gage_weight"] - 1.2
                )
            )

            return [prediction], [100.0]

        updated = update_weights(
            self.weights,
            feedback=feedback,
            enabled=True,
            learning_rate=0.001,
            max_gradient=100.0
        )

        self.assertGreater(
            updated["gage_weight"],
            1.0
        )

    def test_homeostasis(self):

        weights = {
            "gage_weight": 1.49,
            "discharge_weight": 0.51,
            "change_weight": 1.0
        }

        def feedback(candidate):

            prediction = (
                candidate["gage_weight"]
                - candidate["discharge_weight"]
            )

            return [prediction], [10.0]

        updated = update_weights(
            weights,
            feedback=feedback,
            enabled=True,
            learning_rate=1.0
        )

        for value in updated.values():

            self.assertGreaterEqual(
                value,
                0.5
            )

            self.assertLessEqual(
                value,
                1.5
            )

    def test_reject_worse_update(self):

        def feedback(weights):

            prediction = (
                weights["gage_weight"] - 1.0
            )

            return [prediction], [0.0]

        updated = update_weights(
            self.weights,
            feedback=feedback,
            enabled=True
        )

        self.assertEqual(
            updated,
            self.weights
        )


if __name__ == "__main__":
    unittest.main()