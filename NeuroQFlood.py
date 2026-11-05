#!/usr/bin/env python3

"""
NeuroQ-Flood — Adaptive Quantum Forecasting

Compares four forecasting approaches:

1. Persistence
2. Classical
3. Fixed-weight hybrid
4. Adaptive hybrid

Uses historical USGS measurements and
chronological forecasting evaluation.
"""

import argparse

from pathlib import Path

from neuroq.live_memory import (
    load_live_state,
    save_live_state,
    complete_forecasts
)

from neuroq.data_source import (
    download_usgs,
    load_csv,
    get_recent_usgs
)

from neuroq.memory import (
    DEFAULT_WEIGHTS,
    clamp_weights
)

from evaluation.historical_replay import replay

from evaluation.live_forecast import run_live_forecast

from neuroq.live_learning import learn_from_completed

from evaluation.accuracy_metrics import print_metrics

from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent


def main():

    parser = argparse.ArgumentParser(
        description="NeuroQ-Flood adaptive forecasting"
    )

    parser.add_argument(
        "--start",
        default="2024-05-01"
    )

    parser.add_argument(
        "--end",
        default="2024-05-03"
    )

    parser.add_argument(
        "--csv",
        type=Path
    )

    parser.add_argument(
        "--refresh",
        action="store_true"
    )

    parser.add_argument(
        "--weights",
        nargs=3,
        type=float,
        metavar=(
            "GAGE",
            "DISCHARGE",
            "CHANGE"
        ),
        default=[1.0, 1.0, 1.0]
    )

    parser.add_argument(
        "--live",
        action="store_true",
        help="Generate a live 60-minute USGS forecast"
    )

    args = parser.parse_args()

    if args.live:

        state_path = ROOT / "data" / "live" / "live_state.json"

        state = load_live_state(state_path)

        # Restore previously learned weights, if available.
        if state["adaptive_weights"] is not None:

            weights = clamp_weights(
                state["adaptive_weights"]
            )

            print("\nLoaded previously learned quantum weights.")

        else:

            weights = clamp_weights(
                dict(zip(DEFAULT_WEIGHTS, args.weights))
            )

            print("\nUsing initial quantum weights.")

        print("\nRetrieving recent USGS observations...")

        observations = get_recent_usgs(days=14)

        # Verify previously issued forecasts.
        newly_completed = complete_forecasts(
            state,
            observations
        )

        if newly_completed:

            print(
                f"\nVerified {len(newly_completed)} "
                "previously saved forecast(s)."
            )

            for forecast in newly_completed:

                print(
                    f"\nForecast: {forecast['forecast_id']}"
                )

                print(
                    f"Predicted: "
                    f"{forecast['prediction_cfs']:.2f} cfs"
                )

                print(
                    f"Actual: "
                    f"{forecast['actual_discharge_cfs']:.2f} cfs"
                )

                print(
                    f"Absolute error: "
                    f"{forecast['absolute_error_cfs']:.2f} cfs"
                )

                print(
                    "Eligible for learning:",
                    forecast["eligible_for_learning"]
                )

        else:

            print(
                "\nNo previously saved forecasts "
                "ready for verification."
            )

        # Apply learning only to eligible, unprocessed forecasts.
        updated_weights, processed = learn_from_completed(
            state,
            weights
        )

        weights = updated_weights

        if processed:

            print(
                f"\nAdaptive learning processed "
                f"{processed} completed forecast(s)."
            )

            print(
                "Updated quantum weights:",
                weights
            )

        else:

            print(
                "\nNo new eligible forecasts "
                "available for adaptive learning."
            )

        # Persist weights and processed-forecast markers together.
        state["adaptive_weights"] = weights

        save_live_state(state_path, state)

                # Generate the next live forecast using current weights.
        try:

            result = run_live_forecast(
                weights,
                days=14
            )

        except RuntimeError as error:

            if "too old" not in str(error):
                raise

            print("\n" + "=" * 60)
            print("NEUROQ-FLOOD — LIVE FORECAST UNAVAILABLE")
            print("=" * 60)

            print("\nReason:", error)

            print(
                "\nPreviously completed forecasts "
                "have still been verified."
            )

            print(
                "Adaptive weights and learning "
                "history remain saved."
            )

            print(
                "\nTry again when newer USGS "
                "observations become available."
            )

            print("=" * 60)

            return

        forecast_id = (
            f"{result['station']}_"
            f"{result['observation_time'].isoformat()}"
        )

        existing_ids = {
            record["forecast_id"]
            for record in (
                state["pending_forecasts"]
                + state["completed_forecasts"]
            )
        }

        if forecast_id not in existing_ids:

            record = {
                "forecast_id": forecast_id,
                "issued_at": datetime.now(timezone.utc).isoformat(),
                "station": result["station"],
                "observation_timestamp":
                    result["observation_time"].isoformat(),
                "target_timestamp":
                    result["forecast_time"].isoformat(),
                "prediction_cfs":
                    result["hybrid_forecast_cfs"],
                "current_discharge_cfs":
                    result["current_discharge_cfs"],
                "weights": result["weights"],
                "inputs": result["inputs"],
                "trends": result["trends"],
                "availability": result["availability"],
                "model_state": result["model_state"],
            }

            issued_at = datetime.fromisoformat(
                record["issued_at"]
            )

            target_at = datetime.fromisoformat(
                record["target_timestamp"]
            )

            if issued_at >= target_at:

                raise RuntimeError(
                    "Cannot save a forecast issued "
                    "at or after its target timestamp."
                )

            state["pending_forecasts"].append(record)

            save_live_state(state_path, state)

            print("\nLive forecast saved to memory.")

        else:

            print(
                "\nForecast already recorded; "
                "skipping duplicate."
            )

        print("\n" + "=" * 60)
        print("NEUROQ-FLOOD — LIVE ADAPTIVE FORECAST")
        print("=" * 60)

        print("\nStation:", result["station"])
        print("Observation:", result["observation_time"])
        print("Forecast target:", result["forecast_time"])

        print(
            "\nCurrent discharge:",
            result["current_discharge_cfs"],
            "cfs"
        )

        print(
            "Gage height:",
            result["gage_height_ft"],
            "ft"
        )

        print("\n60-MINUTE FORECASTS")
        print("-" * 60)

        print(
            f"Persistence: "
            f"{result['persistence_forecast_cfs']:.2f} cfs"
        )

        print(
            f"Classical: "
            f"{result['classical_forecast_cfs']:.2f} cfs"
        )

        print(
            f"Quantum hybrid: "
            f"{result['hybrid_forecast_cfs']:.2f} cfs"
        )

        print(
            "\nTraining examples:",
            result["training_examples"]
        )

        print(
            "Measurements:",
            result["measurements"]
        )

        print(
            "Quantum weights:",
            weights
        )

        print(
            "\nCompleted forecasts:",
            len(state["completed_forecasts"])
        )

        print(
            "Pending forecasts:",
            len(state["pending_forecasts"])
        )

        print(
            "\nNOTE: Adaptive learning uses only "
            "eligible completed forecasts."
        )

        print("=" * 60)

        return

    cache = (
        args.csv
        or ROOT
        / "data"
        / "historical"
        / (
            f"usgs_08074000_"
            f"{args.start}_{args.end}.csv"
        )
    )

    if (
        args.csv is None
        and (
            args.refresh
            or not cache.exists()
        )
    ):

        print(
            "\nDownloading historical USGS data..."
        )

        count = download_usgs(
            args.start,
            args.end,
            cache
        )

        print(
            f"Downloaded {count} measurements."
        )

    rows = load_csv(cache)

    weights = clamp_weights(
        dict(
            zip(
                DEFAULT_WEIGHTS,
                args.weights
            )
        )
    )

    output = (
        ROOT
        / "data"
        / "results"
        / (
            cache.stem
            + "_adaptive_comparison.csv"
        )
    )

    print("\n" + "=" * 60)

    print(
        "NEUROQ-FLOOD ADAPTIVE FORECASTING"
    )

    print("=" * 60)

    print(
        f"\nMeasurements loaded: {len(rows)}"
    )

    print(
        "\nForecast horizon: 60 minutes"
    )

    print(
        "\nModels: Persistence, Classical, "
        "Fixed Hybrid, Adaptive Hybrid"
    )

    print(
        "\nRunning historical replay..."
    )

    result = replay(
        rows,
        weights,
        output
    )

    print("\n" + "=" * 60)

    print(
        "HISTORICAL REPLAY COMPLETE"
    )

    print("=" * 60)

    print(
        "\nMeasurements processed: "
        f"{result['measurements']}"
    )

    print(
        "Training examples: "
        f"{result['training_examples']}"
    )

    print(
        "Evaluated test forecasts: "
        f"{result['test_forecasts']}"
    )

    print(
        f"\nInitial quantum weights: {weights}"
    )

    print(
        "Final adaptive weights: "
        f"{result['adaptive_weights']}"
    )

    print(
        "Accepted adaptive updates: "
        f"{result['adaptive_updates']}"
    )

    print_metrics(
        "PERSISTENCE BASELINE",
        result["persistence_metrics"]
    )

    print_metrics(
        "CLASSICAL FORECASTING",
        result["classical_metrics"]
    )

    print_metrics(
        "FIXED-WEIGHT HYBRID",
        result["hybrid_metrics"]
    )

    print_metrics(
        "ADAPTIVE HYBRID",
        result["adaptive_metrics"]
    )

    results = {

        "Persistence":
            result["persistence_metrics"]["RMSE"],

        "Classical":
            result["classical_metrics"]["RMSE"],

        "Fixed Hybrid":
            result["hybrid_metrics"]["RMSE"],

        "Adaptive Hybrid":
            result["adaptive_metrics"]["RMSE"]

    }

    winner = min(
        results,
        key=results.get
    )

    print("\n" + "=" * 60)

    print("FORECASTING COMPARISON")

    print("=" * 60)

    for model, rmse in results.items():

        print(
            f"{model}: {rmse:.3f} cfs RMSE"
        )

    print(
        f"\nLowest RMSE: {winner}"
    )

    fixed_rmse = results["Fixed Hybrid"]

    adaptive_rmse = results["Adaptive Hybrid"]

    if adaptive_rmse < fixed_rmse:

        print(
            "\nAdaptive learning improved RMSE "
            "relative to fixed quantum weights."
        )

    elif adaptive_rmse > fixed_rmse:

        print(
            "\nAdaptive learning did not improve "
            "RMSE relative to fixed quantum weights."
        )

    else:

        print(
            "\nAdaptive and fixed hybrid models "
            "achieved equal RMSE."
        )

    print("\nResults saved to:")

    print(output)

    print(
        "\nNOTE: Adaptive learning updates quantum "
        "encoding weights only."
    )

    print(
        "Risk thresholds are not yet "
        "historically calibrated."
    )


if __name__ == "__main__":
    main()