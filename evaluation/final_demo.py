"""
NeuroQ-Flood — Final University Presentation

Displays previously recorded experimental results.
Does not retrieve live data, submit IBM Quantum jobs,
modify model weights, or create forecasts.
"""

WIDTH = 76


def heading(title):
    print("\n" + "=" * WIDTH)
    print(title.center(WIDTH))
    print("=" * WIDTH)


def section(title):
    print("\n" + "-" * WIDTH)
    print(title)
    print("-" * WIDTH)


def row(label, value):
    print(f"{label:<32} {value}")


def overview():
    heading("NEUROQ-FLOOD")
    print("ADAPTIVE QUANTUM-HYBRID FLOOD FORECASTING".center(WIDTH))

    section("PROJECT OVERVIEW")
    row("Monitoring station", "USGS 08074000")
    row("Location", "Buffalo Bayou, Houston, Texas")
    row("Forecast horizon", "60 minutes")
    row("Quantum circuit", "3 qubits")
    row("Hardware processor", "IBM ibm_fez")

    section("IMPLEMENTED FUNCTIONALITIES")
    features = [
        "Historical USGS data processing",
        "Live USGS observation retrieval",
        "60-minute river discharge forecasting",
        "Classical regression forecasting",
        "Quantum-hybrid forecasting",
        "Adaptive quantum encoding weights",
        "Automatic forecast verification",
        "IBM Quantum hardware execution",
        "Local simulation vs. hardware comparison",
        "Automated testing",
    ]

    for feature in features:
        print(f"  [OK] {feature}")


def historical_results():
    heading("HISTORICAL FORECASTING PERFORMANCE")

    row("Evaluation period", "July 7-10, 2024")
    row("USGS measurements", "383")
    row("Training examples", "224")
    row("Test forecasts", "150")

    section("MODEL ACCURACY COMPARISON")

    models = [
        ("Persistence", 158.80, 225.76),
        ("Classical Regression", 124.69, 165.88),
        ("Fixed Quantum Hybrid", 228.26, 256.38),
        ("Adaptive Quantum Hybrid", 76.13, 111.79),
    ]

    print(f"{'MODEL':<30}{'MAE (cfs)':>15}{'RMSE (cfs)':>15}")
    print("-" * 60)

    for name, mae, rmse in models:
        print(f"{name:<30}{mae:>15.2f}{rmse:>15.2f}")

    section("KEY RESULTS")

    improvement = (165.88 - 111.79) / 165.88 * 100

    row("Best model", "Adaptive Quantum Hybrid")
    row("Best MAE", "76.13 cfs")
    row("Best RMSE", "111.79 cfs")
    row("Nash-Sutcliffe Efficiency", "0.9707")
    row("RMSE improvement vs. classical", f"{improvement:.2f}%")

    print("\nResults are specific to this historical evaluation period.")


def adaptive_learning():
    heading("ADAPTIVE QUANTUM LEARNING")

    section("HISTORICAL LEARNING RESULTS")
    row("Test forecasts", "150")
    row("Accepted adaptive updates", "104")

    section("HOW ADAPTIVE LEARNING WORKS")
    steps = [
        "1. Generate a 60-minute discharge forecast.",
        "2. Retrieve the actual observation when available.",
        "3. Calculate the forecasting error.",
        "4. Evaluate candidate quantum weight adjustments.",
        "5. Accept beneficial updates and save the weights.",
        "6. Apply the updated weights to future forecasts.",
    ]

    for step in steps:
        print(step)

    section("VERIFIED LIVE WEIGHT UPDATE")

    print(f"{'INPUT':<30}{'BEFORE':>15}{'AFTER':>15}")
    print("-" * 60)

    weights = [
        ("Gage Height", 1.0, 0.9),
        ("Discharge", 1.0, 1.1),
        ("Water-Level Change", 1.0, 1.0),
    ]

    for name, before, after in weights:
        print(f"{name:<30}{before:>15.2f}{after:>15.2f}")


def live_results():
    heading("LIVE FORECASTING RESULTS")

    section("VERIFIED FORECAST — NOVEMBER 19, 2026")

    predicted = 293.55
    actual = 301.00
    absolute_error = abs(actual - predicted)
    percentage_error = absolute_error / actual * 100

    row("Monitoring station", "USGS 08074000")
    row("Forecast target", "2:15 PM CST")
    row("Predicted discharge", f"{predicted:.2f} cfs")
    row("Observed discharge", f"{actual:.2f} cfs")
    row("Absolute error", f"{absolute_error:.2f} cfs")
    row("Percentage error", f"{percentage_error:.2f}%")

    section("LIVE SYSTEM CAPABILITIES")
    row("Retrieve current USGS data", "SUPPORTED")
    row("Generate 60-minute forecasts", "SUPPORTED")
    row("Verify pending forecasts", "SUPPORTED")
    row("Calculate forecast errors", "SUPPORTED")
    row("Update quantum weights", "SUPPORTED")
    row("Persist adaptive learning state", "SUPPORTED")

    print("\nThis is one previously verified live forecast.")


def quantum_results():
    heading("IBM QUANTUM HARDWARE VALIDATION")

    section("QUANTUM CIRCUIT")

    row("Qubits", "3")
    row("Input 1", "Gage height")
    row("Input 2", "Discharge")
    row("Input 3", "Water-level change")
    row("Encoding gates", "RY rotations")
    row("Entanglement", "CX(0,1), CX(1,2)")
    row("Measurements per experiment", "1,024")

    section("REAL HARDWARE EXPERIMENTS")

    print(
        f"{'MEASUREMENT':<30}"
        f"{'EXPERIMENT 1':>18}"
        f"{'EXPERIMENT 2':>18}"
    )
    print("-" * 66)

    experiments = [
        ("Local simulation score", 35.1123, 30.6464),
        ("IBM hardware score", 32.8776, 31.3477),
        ("Absolute difference", 2.2347, 0.7012),
    ]

    for name, first, second in experiments:
        print(f"{name:<30}{first:>18.4f}{second:>18.4f}")

    section("IBM QUANTUM JOB RECORDS")
    row("Processor", "ibm_fez")
    row("Experiment 1 job", "dbvli22nj2vs73dcpmq0")
    row("Experiment 2 job", "dbvmg85hdvas73bib7bg")
    row("Successful hardware executions", "2")

    print("\nHardware execution validates the circuit implementation.")
    print("It does not establish a quantum forecasting advantage.")


def testing_results():
    heading("SYSTEM TESTING AND VALIDATION")

    section("AUTOMATED TEST RESULTS")
    row("Existing system tests", "21")
    row("IBM Quantum integration tests", "12")
    row("Total tests", "33")
    row("Passed", "33")
    row("Failed", "0")

    section("TESTED COMPONENTS")

    components = [
        "Adaptive learning",
        "Forecasting pipeline",
        "Historical replay",
        "Data leakage prevention",
        "Training normalization",
        "Quantum circuit construction",
        "Local simulator vs. Qiskit",
        "Quantum measurement scoring",
        "Mocked IBM hardware execution",
    ]

    for component in components:
        print(f"  [PASS] {component}")

    print("\nFINAL RESULT: 33 / 33 TESTS PASSED")


def conclusion():
    heading("NEUROQ-FLOOD — FINAL RESULTS")

    print("""
PROJECT ACCOMPLISHMENTS

  [OK] Functional 60-minute river discharge forecasting
  [OK] Classical and quantum-hybrid model comparison
  [OK] Adaptive learning from verified observations
  [OK] Real-time USGS integration
  [OK] Two successful IBM Quantum hardware experiments
  [OK] 33 passing automated tests

KEY RESEARCH FINDING

  Adaptive quantum-hybrid forecasting achieved a
  32.61% lower RMSE than classical regression
  during the July 2024 historical evaluation.

IMPORTANT LIMITATION

  Normal forecasting uses local quantum simulation.
  IBM hardware is used for separate circuit validation.

  These results do not demonstrate universal model
  superiority or a proven quantum advantage.
""")

    print("=" * WIDTH)
    print("END OF NEUROQ-FLOOD PRESENTATION".center(WIDTH))
    print("=" * WIDTH)


def main():
    overview()
    historical_results()
    adaptive_learning()
    live_results()
    quantum_results()
    testing_results()
    conclusion()


if __name__ == "__main__":
    main()