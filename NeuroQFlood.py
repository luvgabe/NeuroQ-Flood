#!/usr/bin/env python3

"""
NeuroQ-Flood — Week 10 Forecasting Comparison

Historical USGS flood forecasting.

Compares:
1. Persistence baseline
2. Classical forecasting
3. Hybrid quantum-classical forecasting

Uses chronological training/testing
and a 60-minute forecast horizon.
"""

import argparse

from pathlib import Path

from neuroq.data_source import (
    download_usgs,
    load_csv
)

from neuroq.memory import (
    DEFAULT_WEIGHTS,
    clamp_weights
)

from evaluation.historical_replay import replay

from evaluation.accuracy_metrics import print_metrics


ROOT = Path(__file__).resolve().parent


def main():

    parser = argparse.ArgumentParser(
        description="NeuroQ-Flood forecasting comparison"
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

    args = parser.parse_args()

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
            + "_model_comparison.csv"
        )
    )

    print("\n" + "=" * 60)

    print(
        "NEUROQ-FLOOD MODEL COMPARISON"
    )

    print("=" * 60)

    print(
        f"\nMeasurements loaded: {len(rows)}"
    )

    print(
        "\nForecast horizon: 60 minutes"
    )

    print(
        "\nModels: Persistence, Classical, Hybrid"
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
        f"\nQuantum encoding weights: {weights}"
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
        "HYBRID NEUROQ-FLOOD FORECASTING",
        result["hybrid_metrics"]
    )

    results = {

        "Persistence":
            result["persistence_metrics"]["RMSE"],

        "Classical":
            result["classical_metrics"]["RMSE"],

        "Hybrid NeuroQ-Flood":
            result["hybrid_metrics"]["RMSE"]

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

    classical_rmse = results["Classical"]

    hybrid_rmse = results["Hybrid NeuroQ-Flood"]

    if hybrid_rmse < classical_rmse:

        print(
            "\nQuantum features improved RMSE "
            "relative to the classical model."
        )

    elif hybrid_rmse > classical_rmse:

        print(
            "\nQuantum features did not improve "
            "RMSE relative to the classical model."
        )

    else:

        print(
            "\nClassical and hybrid models "
            "achieved equal RMSE."
        )

    print("\nResults saved to:")

    print(output)

    print(
        "\nNOTE: Automatic adaptive learning "
        "is not yet implemented."
    )

    print(
        "Risk thresholds are not yet "
        "historically calibrated."
    )


if __name__ == "__main__":
    main()