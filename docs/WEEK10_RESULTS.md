# NeuroQ-Flood — Week 10 Results

## 1. Overview

During Week 10, NeuroQ-Flood was extended with automatic,
feedback-driven adaptation of quantum encoding weights.

The system now compares four one-hour-ahead discharge
forecasting approaches:

1. Persistence baseline
2. Classical forecasting
3. Fixed-weight hybrid quantum-classical forecasting
4. Adaptive hybrid quantum-classical forecasting

The objective was to implement adaptive learning,
evaluate its forecasting performance, and investigate
whether weight optimization improves prediction accuracy.

## 2. Implementation

### Adaptive Quantum Learning

Implemented an adaptive optimizer that adjusts three
quantum encoding weights:

- Gage height weight
- Discharge weight
- Water-change weight

Weight updates are driven by forecasting errors from
completed historical predictions.

The optimizer evaluates candidate weights against a
rolling window of recent forecasting observations.

### Homeostasis

Adaptive weights are constrained to the interval:

0.5 <= weight <= 1.5

This prevents unrestricted changes to quantum encoding
parameters.

### Historical Replay

The historical replay pipeline was extended to compare
four forecasting approaches on identical evaluation
timestamps.

The adaptive model updates its quantum encoding weights
when historical forecast targets become available.

The regression coefficients remain fixed during
adaptive learning.

## 3. Automated Testing

The project passed 21 automated tests.

These include tests for:

- Adaptive learning behavior
- Homeostasis constraints
- Persistent memory
- Quantum feature generation
- Discharge trend calculations
- Forecasting metrics
- Historical replay
- Future-observation independence
- Matching evaluation timestamps

Result:

21 tests passed.

The data-leakage tests provide targeted verification
of chronological behavior but do not establish a
complete absence of all possible data leakage.

## 4. Historical Evaluation

USGS station: 08074000

Location: Buffalo Bayou, Houston, Texas

Forecast horizon: 60 minutes

### Experiment A — May 1–3, 2024

Measurements: 287
Training examples: 167
Test forecasts: 111

| Model | MAE (cfs) | RMSE (cfs) | NSE |
|---|---:|---:|---:|
| Persistence | 144.432 | 172.656 | 0.9669 |
| Classical | 54.678 | 77.250 | 0.9934 |
| Fixed hybrid | 98.497 | 132.192 | 0.9806 |
| Adaptive hybrid | 52.097 | 70.667 | 0.9944 |

Adaptive learning reduced RMSE by approximately 46.5%
relative to the fixed-weight hybrid.

The adaptive hybrid also achieved approximately 8.5%
lower RMSE than the classical model.

Accepted adaptive updates: 72

Final adaptive weights:

- Gage: 0.6
- Discharge: 1.0
- Water change: 1.5

### Experiment B — May 1–3, 2025

Measurements: 286
Training examples: 167
Test forecasts: 109

| Model | MAE (cfs) | RMSE (cfs) | NSE |
|---|---:|---:|---:|
| Persistence | 55.593 | 85.075 | 0.7525 |
| Classical | 125.342 | 167.329 | 0.0426 |
| Fixed hybrid | 137.616 | 181.558 | -0.1272 |
| Adaptive hybrid | 155.077 | 201.558 | -0.3892 |

The persistence baseline achieved the lowest RMSE.

The adaptive hybrid performed worse than both the
classical and fixed-weight hybrid approaches.

Accepted adaptive updates: 76

Final adaptive weights:

- Gage: 1.4
- Discharge: 0.5
- Water change: 0.5

## 5. Findings

The adaptive learning mechanism successfully modified
quantum encoding weights in response to forecasting
errors while respecting homeostatic constraints.

However, forecasting improvements were not consistent
across the two historical periods.

The May 2024 experiment demonstrated improved
performance, while the May 2025 experiment revealed
limitations in model generalization.

Potential contributing factors include:

- Differences in hydrological conditions
- Limited training data
- Changes in quantum feature distributions
- Fixed regression coefficients during adaptation
- Sensitivity to the recent-feedback window

These explanations require further investigation.

## 6. Limitations

The quantum circuit is classically simulated.

The results do not demonstrate quantum computational
advantage.

Adaptive learning is evaluated using a chronological
predict-then-learn procedure rather than a completely
frozen holdout evaluation.

Additional testing across independent historical events
is necessary before claiming reliable improvements.

Risk thresholds have not yet been historically calibrated.

## 7. Week 10 Conclusion

Week 10 successfully integrated automatic adaptive
quantum-weight learning into NeuroQ-Flood.

The system passed 21 automated tests and completed
two historical forecasting experiments.

Results demonstrate that adaptive weight optimization
is operational, while also revealing that forecasting
performance depends on the historical evaluation period.

Future development will focus on improving robustness,
generalization, and validation across additional
hydrological conditions.