# NeuroQ-Flood
### Adaptive Quantum-Hybrid Flood Forecasting

**NeuroQ-Flood** is an experimental, bio-inspired, quantum-hybrid flood forecasting system developed in Python.

The project investigates whether adaptive quantum feature encoding can improve short-term river discharge forecasting compared with classical regression and fixed-weight quantum-hybrid approaches.

NeuroQ-Flood combines:

- Real-world hydrological observations from the United States Geological Survey (USGS)
- Classical regression forecasting
- Three-qubit quantum feature encoding
- Neuroplasticity-inspired adaptive learning
- Automatic forecast verification
- Historical forecasting experiments
- Live 60-minute discharge predictions
- Optional IBM Quantum hardware execution
- Automated software testing

The system monitors **USGS station 08074000**, located along Buffalo Bayou in Houston, Texas.

Its primary forecasting objective is to predict river discharge **60 minutes into the future**, measured in cubic feet per second (cfs).

> **Research Disclaimer**
>
> NeuroQ-Flood is an educational research prototype. It is not an official flood warning system and must not be used for emergency response, evacuation decisions, or public-safety planning.

---

# 1. Project Overview

## 1.1 Research Motivation

Flood forecasting is challenging because river conditions change over time.

Traditional forecasting methods rely on historical observations, statistical models, and environmental measurements to estimate future hydrological conditions.

However, forecasting performance may vary across different environmental conditions.

NeuroQ-Flood investigates whether a hybrid architecture combining classical regression, quantum-derived features, and adaptive learning can provide an alternative approach to short-term discharge forecasting.

The project is inspired by biological neuroplasticity: the ability of biological systems to adjust their behavior in response to experience.

In NeuroQ-Flood, this concept is implemented through adjustable quantum encoding weights that respond to completed forecast errors.

## 1.2 Research Objectives

The project investigates five primary questions:

1. Can historical USGS observations support accurate 60-minute discharge forecasting?
2. How does classical regression compare with quantum-hybrid forecasting?
3. Can adaptive quantum encoding improve performance relative to fixed quantum encoding?
4. Can forecast errors automatically guide future weight adjustments?
5. Can the quantum circuit used by the system execute successfully on real IBM Quantum hardware?

The project does not attempt to prove that quantum computing universally outperforms classical forecasting.

Instead, it evaluates the potential of adaptive quantum-hybrid architectures through controlled historical experiments, live forecasting, and circuit-level hardware validation.

---

# 2. Implemented Capabilities

The completed NeuroQ-Flood implementation supports:

| Capability | Status |
|---|---|
| Historical USGS data retrieval | Implemented |
| Historical CSV processing | Implemented |
| Hydrological preprocessing | Implemented |
| Classical regression forecasting | Implemented |
| Quantum-hybrid forecasting | Implemented |
| Adaptive quantum encoding | Implemented |
| Historical forecast replay | Implemented |
| Chronological training/testing | Implemented |
| Automatic forecast verification | Implemented |
| Live 60-minute forecasting | Implemented |
| Persistent adaptive learning | Implemented |
| IBM Quantum hardware execution | Implemented |
| Local simulation vs. hardware comparison | Implemented |
| Automated testing | Implemented |
| IL-KAN research comparison | Documented |

---

# 3. System Architecture

NeuroQ-Flood uses a hybrid architecture combining environmental measurements, classical forecasting, quantum-derived features, and adaptive feedback.

```text
                    USGS HYDROLOGICAL DATA
                              |
                              v
                     DATA PREPROCESSING
                              |
                              v
                      FEATURE EXTRACTION
                              |
                 +------------+------------+
                 |                         |
                 v                         v
          CLASSICAL FEATURES        QUANTUM ENCODING
                 |                         |
                 |                   THREE QUBITS
                 |                         |
                 |                    RY ROTATIONS
                 |                         |
                 |                     CX GATES
                 |                         |
                 |                  QUANTUM SCORE
                 |                         |
                 +------------+------------+
                              |
                              v
                    HYBRID REGRESSION
                              |
                              v
                    60-MINUTE FORECAST
                              |
                              v
                    FUTURE OBSERVATION
                              |
                              v
                    FORECAST VERIFICATION
                              |
                              v
                     ERROR CALCULATION
                              |
                              v
                     ADAPTIVE LEARNING
                              |
                              v
                   UPDATED QUANTUM WEIGHTS
                              |
                              +------> FUTURE FORECASTS
```

The system uses classical processing for data retrieval, normalization, regression, and forecast evaluation.

Quantum-derived features provide an additional representation of the hydrological inputs.

Adaptive learning adjusts the quantum encoding weights based on completed forecasting errors.

---

# 4. Forecasting Models

NeuroQ-Flood evaluates four forecasting approaches.

## 4.1 Persistence Baseline

The persistence baseline assumes that river discharge remains unchanged over the forecasting horizon.

```text
Predicted discharge at t + 60 minutes
=
Observed discharge at time t
```

This provides a simple reference against which more advanced models can be evaluated.

## 4.2 Classical Regression

The classical model uses hydrological measurements and derived features to predict future discharge.

It does not include quantum-derived features.

## 4.3 Fixed-Weight Quantum Hybrid

The fixed hybrid model combines classical forecasting features with a quantum-derived score.

The quantum encoding weights remain constant during evaluation.

## 4.4 Adaptive Quantum Hybrid

The adaptive hybrid model uses the same trained regression coefficients as the fixed hybrid model.

However, its quantum encoding weights can change based on completed forecast errors.

**Important:** Adaptive learning modifies quantum encoding weights, not the trained regression coefficients.

This distinction allows the project to investigate whether adaptive feature encoding can improve forecasting without continuously retraining the entire regression model.

---

# 5. Quantum Computing Architecture

## 5.1 Three-Qubit Representation

NeuroQ-Flood uses three hydrological inputs in its quantum representation:

| Qubit | Environmental Feature |
|---|---|
| Qubit 0 | Gage height |
| Qubit 1 | River discharge |
| Qubit 2 | Water-level change |

These measurements are normalized before being encoded into quantum rotation angles.

## 5.2 Quantum Circuit

The circuit uses:

- Three qubits
- RY rotation gates
- Two CX entanglement gates
- Measurement of all three qubits

Conceptually:

```text
q0: ──RY(θ0)──■────────────────M
              |
q1: ──RY(θ1)──X────■───────────M
                   |
q2: ──RY(θ2)───────X───────────M
```

The entanglement operations are:

```text
CX(0, 1)
CX(1, 2)
```

The local quantum implementation calculates a quantum-derived score used by the hybrid forecasting system.

## 5.3 Local Simulation vs. Real Hardware

Normal NeuroQ-Flood forecasting uses local quantum simulation.

Real IBM Quantum hardware is used through a separate optional comparison workflow.

The hardware experiment validates that the corresponding quantum circuit can execute on a physical quantum processor.

**The complete forecasting pipeline is not executed on IBM Quantum hardware.**

No quantum computational advantage has been established.

---

# 6. Adaptive Learning

## 6.1 Biological Inspiration

NeuroQ-Flood's adaptive mechanism is inspired by neuroplasticity.

Rather than treating all feature contributions as permanently fixed, the system allows selected encoding weights to change in response to forecasting performance.

The adjustable parameters are:

```text
gage_weight
discharge_weight
change_weight
```

## 6.2 Learning Process

The adaptive learning cycle is:

```text
1. Generate a forecast.
2. Wait until the forecast target time.
3. Obtain the actual discharge observation.
4. Calculate the forecasting error.
5. Evaluate candidate weight adjustments.
6. Accept beneficial adjustments.
7. Save the updated weights.
8. Use them in future forecasts.
```

Forecasts are not eligible for feedback until their corresponding target observations become available.

This helps prevent the system from learning from future observations before they would be available in a real forecasting environment.

## 6.3 Historical Learning Configuration

The historical replay uses:

| Parameter | Value |
|---|---|
| Forecast horizon | 60 minutes |
| Training split | 60% |
| Evaluation split | 40% |
| Feedback memory window | 12 forecasts |
| Learning rate | 0.001 |
| Finite-difference epsilon | 0.001 |
| Maximum gradient | 100.0 |

Adaptive weights are also constrained using the project's weight-clamping mechanism.

These bounds help prevent unrestricted weight changes.

## 6.4 Persistent Live Learning

Live forecasting uses:

```text
data/live/live_state.json
```

This file stores information needed to maintain the learning process between program executions.

The live workflow can:

- Restore previously learned weights
- Identify forecasts awaiting verification
- Match forecasts with available observations
- Calculate completed forecast errors
- Apply eligible adaptive updates
- Track already-processed forecasts
- Save updated learning state

Because this state persists, restarting the program does not necessarily reset its learning history.

**Do not delete or overwrite the live state file unless you intentionally want to reset the stored forecasting history.**

---

# 7. Technologies and Dependencies

NeuroQ-Flood is implemented primarily in Python.

The core forecasting, preprocessing, historical replay, and adaptive learning components use Python's standard library.

Optional IBM Quantum integration requires:

| Dependency | Version | Purpose |
|---|---|---|
| Qiskit | 2.5.2 | Quantum circuit construction and transpilation |
| Qiskit IBM Runtime | 0.52.1 | IBM Quantum hardware execution |
| pytest | 9.2.0 | Automated testing |

The two Qiskit packages are specified in:

```text
requirements.txt
```

pytest is installed separately for development and testing.

---

# 8. Repository Structure

```text
Neuro-Q-Flood/
|
|-- NeuroQFlood.py
|-- README.md
|-- requirements.txt
|-- adaptive_weights.json
|-- .gitignore
|
|-- neuroq/
|   |-- __init__.py
|   |-- adaptive_learning.py
|   |-- data_source.py
|   |-- forecasting.py
|   |-- ibm_quantum.py
|   |-- live_learning.py
|   |-- live_memory.py
|   |-- memory.py
|   |-- mitigation.py
|   |-- preprocessing.py
|   |-- quantum_model.py
|   |-- risk_assessment.py
|
|-- evaluation/
|   |-- __init__.py
|   |-- accuracy_metrics.py
|   |-- compare_ilkan.py
|   |-- final_demo.py
|   |-- historical_replay.py
|   |-- ibm_comparison.py
|   |-- live_forecast.py
|   |-- usgs_quality_check.py
|
|-- tests/
|   |-- __init__.py
|   |-- test_adaptive_learning.py
|   |-- test_data_leakage.py
|   |-- test_ibm_quantum.py
|   |-- test_pipeline.py
|
|-- data/
|   |-- historical/
|   |-- live/
|   |-- results/
|
|-- docs/
|   |-- WEEK10_RESULTS.md
|   |-- WEEK11_DELIVERABLE.md
|   |-- WEEK11_ILKAN_COMPARISON.md
|   |-- WEEK12_README.md
```

## Important Files

### `NeuroQFlood.py`

The main command-line application.

It provides historical forecasting, live forecasting, and optional IBM Quantum execution.

### `neuroq/forecasting.py`

Implements the forecasting model and feature extraction.

### `neuroq/quantum_model.py`

Implements the local quantum feature calculation.

### `neuroq/adaptive_learning.py`

Implements the adaptive weight-update mechanism.

### `neuroq/live_learning.py`

Processes eligible completed forecasts for live adaptive learning.

### `neuroq/live_memory.py`

Handles persistent live forecasting state.

### `evaluation/historical_replay.py`

Runs chronological historical forecasting and compares four models.

### `evaluation/ibm_comparison.py`

Compares local quantum simulation with IBM Quantum hardware.

### `evaluation/final_demo.py`

Displays previously recorded project results for demonstration purposes.

It does not generate new forecasts or submit hardware jobs.

---

# 9. Installation and Setup

## 9.1 Prerequisites

Install:

- Python 3
- Git
- A terminal or command-line environment

A Python virtual environment is recommended.

## 9.2 Clone the Repository

Clone the NeuroQ-Flood repository:

```bash
git clone https://github.com/luvgabe/NeuroQ-FloodL
```

Navigate into the directory containing `NeuroQFlood.py`:

```bash
cd NeuroQ-FloodL
```

The exact directory name depends on how the repository was cloned or organized.

## 9.3 Create a Virtual Environment

### macOS / Linux

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
py -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 9.4 Install Dependencies

With the virtual environment activated:

```bash
python -m pip install --upgrade pip
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

Install the testing framework:

```bash
python -m pip install pytest==9.2.0
```

## 9.5 Verify Installation

Check Python:

```bash
python --version
```

Check pytest:

```bash
python -m pytest --version
```

Check the main application:

```bash
python NeuroQFlood.py --help
```

The help output should include:

```text
--start
--end
--csv
--refresh
--weights
--live
--ibm-quantum
--backend
--shots
```

If these options appear, the main command-line interface is available.

---

# 10. Running Historical Forecasting

Historical forecasting is the recommended starting point for evaluating NeuroQ-Flood.

It does not require IBM Quantum credentials.

## 10.1 Run the Default Historical Experiment

Execute:

```bash
python NeuroQFlood.py
```

By default, the application uses:

```text
Start date: 2024-05-01
End date:   2024-05-03
```

The application loads the corresponding historical USGS dataset.

If the expected cached dataset is missing, it attempts to download the observations.

The system then:

1. Loads the measurements.
2. Sorts and prepares the data.
3. Fits normalization ranges using training observations.
4. Trains the classical and fixed hybrid regression models.
5. Evaluates the four forecasting approaches.
6. Processes completed forecasts for adaptive learning.
7. Calculates forecasting accuracy.
8. Saves the detailed results.

## 10.2 Run the July 2024 Experiment

The July 2024 experiment is one of the project's primary recorded evaluations.

Execute:

```bash
python NeuroQFlood.py --start 2024-07-07 --end 2024-07-10
```

This experiment evaluates the period associated with the project's July 2024 results.

## 10.3 Run Additional Historical Periods

The repository contains historical datasets for several evaluation periods.

Examples:

```bash
python NeuroQFlood.py --start 2024-01-15 --end 2024-01-17
```

```bash
python NeuroQFlood.py --start 2024-05-01 --end 2024-05-03
```

```bash
python NeuroQFlood.py --start 2025-05-01 --end 2025-05-03
```

```bash
python NeuroQFlood.py --start 2025-07-01 --end 2025-07-04
```

These experiments help demonstrate that model performance varies across different historical periods.

## 10.4 Use a Custom Historical CSV

To run an experiment using a local dataset:

```bash
python NeuroQFlood.py --csv data/historical/usgs_08074000_2024-07-07_2024-07-10.csv
```

The CSV must follow the format expected by the project's data-loading implementation.

## 10.5 Refresh Historical Data

To request a fresh download:

```bash
python NeuroQFlood.py --start 2024-07-07 --end 2024-07-10 --refresh
```

This requests data from USGS instead of relying on the existing cache.

**Warning:** Refreshing historical data may replace the cached dataset.

For reproducible experiments, prefer the existing historical files when available.

## 10.6 Specify Initial Quantum Weights

The application supports custom initial encoding weights.

Example:

```bash
python NeuroQFlood.py --weights 1.0 1.0 1.0
```

The values correspond to:

```text
GAGE DISCHARGE CHANGE
```

For example:

```bash
python NeuroQFlood.py --weights 0.9 1.1 1.0
```

These values are processed through the project's weight-clamping mechanism.

## 10.7 Historical Output

Historical results are saved under:

```text
data/results/
```

For the July 2024 experiment, the expected output filename is:

```text
data/results/usgs_08074000_2024-07-07_2024-07-10_adaptive_comparison.csv
```

The output includes:

- Observation timestamps
- Training/test labels
- Gage height
- Discharge
- Discharge trends
- Risk classification
- Forecast target timestamps
- Actual future discharge
- Persistence predictions
- Classical predictions
- Fixed hybrid predictions
- Adaptive hybrid predictions
- Adaptive weight values
- Accepted adaptive update counts

**Warning:** Repeating an experiment using the same output filename overwrites the corresponding results CSV.

---

# 11. Historical Evaluation Methodology

## 11.1 Chronological Split

Historical measurements are ordered by timestamp.

The first 60% are used for training.

The remaining 40% form the evaluation portion.

This avoids randomly mixing earlier and later measurements.

## 11.2 Forecast Horizon

Each forecast targets discharge 60 minutes after the observation timestamp.

A historical target is used only when the corresponding timestamp exists in the loaded observations.

## 11.3 Training

The classical and fixed hybrid models are trained using the training portion of the dataset.

The adaptive hybrid begins with the same trained regression coefficients as the fixed hybrid model.

## 11.4 Adaptive Replay

As historical time advances, forecasts become eligible for feedback when their target timestamps are reached.

The system uses completed forecasts to evaluate potential quantum encoding weight adjustments.

Only the quantum encoding weights adapt.

## 11.5 Evaluation Metrics

NeuroQ-Flood reports forecasting metrics including:

### Mean Absolute Error (MAE)

```text
MAE = mean(|actual - predicted|)
```

MAE measures the average magnitude of forecasting errors.

### Root Mean Squared Error (RMSE)

```text
RMSE = sqrt(mean((actual - predicted)^2))
```

RMSE penalizes larger errors more strongly.

### Nash-Sutcliffe Efficiency (NSE)

```text
NSE = 1 - sum((actual - predicted)^2)
          / sum((actual - mean(actual))^2)
```

NSE compares forecasting performance against a reference based on the mean observed discharge.

Higher NSE generally indicates better agreement with observations.

---

# 12. Recorded Historical Results

The following values are from previously recorded project experiments.

They are not guarantees of performance on other dates or datasets.

## 12.1 July 7–10, 2024

Recorded evaluation:

| Measurement | Value |
|---|---:|
| USGS measurements | 383 |
| Training examples | 224 |
| Test forecasts | 150 |
| Accepted adaptive updates | 104 |

### Forecasting Accuracy

| Model | MAE (cfs) | RMSE (cfs) |
|---|---:|---:|
| Persistence | 158.80 | 225.76 |
| Classical Regression | 124.69 | 165.88 |
| Fixed Quantum Hybrid | 228.26 | 256.38 |
| Adaptive Quantum Hybrid | **76.13** | **111.79** |

The adaptive hybrid achieved:

```text
MAE:  76.13 cfs
RMSE: 111.79 cfs
NSE:  0.9707
```

Compared with classical regression:

```text
RMSE reduction = (165.88 - 111.79) / 165.88 × 100

RMSE reduction ≈ 32.61%
```

Compared with the fixed quantum hybrid:

```text
RMSE reduction = (256.38 - 111.79) / 256.38 × 100

RMSE reduction ≈ 56.4%
```

For this selected period, the adaptive hybrid achieved the lowest RMSE among the four evaluated models.

## 12.2 May 1–3, 2024

A separate recorded historical experiment produced:

| Metric | Adaptive Hybrid |
|---|---:|
| MAE | 52.097 cfs |
| RMSE | 70.667 cfs |
| NSE | 0.9944 |

These results correspond to a different evaluation period.

They should not be interpreted as evidence of consistent performance across all hydrological conditions.

## 12.3 Multi-Period Interpretation

Across five evaluated historical periods:

- The adaptive hybrid improved RMSE relative to the fixed hybrid in four of five periods.
- The adaptive hybrid achieved the lowest RMSE among the evaluated models in two of five periods.

These results suggest that adaptive quantum encoding can improve performance in selected conditions.

However, the improvement is not universal.

---

# 13. Running Live Forecasting

NeuroQ-Flood supports live forecasting using recent USGS observations.

Execute:

```bash
python NeuroQFlood.py --live
```

The application performs one forecasting cycle.

It does not remain running as a continuous background service.

## 13.1 Live Forecasting Workflow

The application:

1. Loads previously saved live state.
2. Restores learned quantum weights if available.
3. Retrieves recent USGS observations.
4. Checks previously issued forecasts.
5. Verifies forecasts whose target observations are available.
6. Calculates forecast errors.
7. Processes eligible forecasts for adaptive learning.
8. Saves updated weights and learning history.
9. Generates a new 60-minute forecast.
10. Saves the forecast if it has not already been recorded.

## 13.2 Live Forecast Output

The terminal displays information such as:

```text
NEUROQ-FLOOD — LIVE ADAPTIVE FORECAST

Station: 08074000

Observation: <timestamp>

Forecast target: <timestamp>

Current discharge: <value> cfs

Gage height: <value> ft

60-MINUTE FORECASTS

Persistence: <value> cfs

Classical: <value> cfs

Quantum hybrid: <value> cfs
```

The actual values depend on the latest available USGS measurements.

## 13.3 Verifying a Previous Forecast

To verify a previously issued forecast, run the live command again after the forecast target observation becomes available:

```bash
python NeuroQFlood.py --live
```

When an eligible observation is available, the application can report:

```text
Verified previously saved forecast

Predicted: <value> cfs

Actual: <value> cfs

Absolute error: <value> cfs

Eligible for learning: True
```

The program may then update the quantum encoding weights.

Verification depends on the availability and timestamps of USGS observations.

Simply waiting 60 minutes does not guarantee that the corresponding observation has already been published.

## 13.4 Recorded Live Forecast

On November 19, 2026, NeuroQ-Flood verified a previously issued forecast.

| Measurement | Value |
|---|---:|
| Monitoring station | USGS 08074000 |
| Forecast target | 2:15 PM CST |
| Predicted discharge | 293.55 cfs |
| Observed discharge | 301.00 cfs |
| Absolute error | 7.45 cfs |
| Percentage error | 2.48% |

This is one verified live forecast.

It does not establish the system's typical live forecasting accuracy.

## 13.5 Recorded Adaptive Weight Update

During the recorded live experiment, the weights changed as follows:

| Feature | Before | After |
|---|---:|---:|
| Gage height | 1.0 | 0.9 |
| Discharge | 1.0 | 1.1 |
| Water-level change | 1.0 | 1.0 |

This demonstrates that the live system can update and preserve its encoding weights after processing eligible completed forecasts.

## 13.6 Live Data Availability

Live forecasting requires recent USGS observations.

If observations are too old, the application may report:

```text
NEUROQ-FLOOD — LIVE FORECAST UNAVAILABLE
```

In this situation, previously completed forecasts may still be verified and adaptive state may still be saved.

Try again when newer observations become available.

---

# 14. IBM Quantum Hardware Integration

IBM Quantum execution is optional.

The core forecasting system can be used without an IBM Quantum account.

## 14.1 Requirements

To execute the hardware comparison, users need:

- The project's Qiskit dependencies
- An IBM Quantum account
- A valid IBM Quantum API key
- An IBM Quantum instance CRN
- Access to the selected hardware backend
- Available IBM Quantum Runtime Units

Hardware availability and account entitlements may change.

## 14.2 Run the Hardware Comparison

Execute:

```bash
python NeuroQFlood.py --ibm-quantum
```

By default, the application uses:

```text
Backend: ibm_fez
Shots: 1024
```

## 14.3 Select a Backend

Example:

```bash
python NeuroQFlood.py --ibm-quantum --backend ibm_fez
```

The selected backend must be accessible through the user's IBM Quantum account.

## 14.4 Change the Measurement Count

Example:

```bash
python NeuroQFlood.py --ibm-quantum --shots 1024
```

The shot count must be greater than zero.

## 14.5 Hardware Execution Workflow

The application:

1. Retrieves recent USGS measurements.
2. Normalizes the hydrological inputs.
3. Loads available adaptive quantum weights.
4. Calculates a local quantum score.
5. Constructs the corresponding rotation angles.
6. Displays the hardware configuration.
7. Warns about IBM Quantum Runtime Unit consumption.
8. Requests explicit confirmation.
9. Prompts for IBM credentials.
10. Submits the quantum circuit.
11. Retrieves measurement counts.
12. Calculates the hardware score.
13. Compares the hardware and local scores.

## 14.6 Hardware Confirmation

Before submitting a job, the application asks:

```text
Submit this experiment to IBM hardware? (yes/no):
```

Enter:

```text
yes
```

to continue.

Any other response cancels the hardware submission.

**Warning:** Hardware jobs may consume limited account resources.

## 14.7 IBM Authentication

The application requests:

```text
IBM Quantum API key:
IBM Quantum instance CRN:
```

These values are entered using Python's `getpass()` functionality.

The credentials are not visibly echoed in the terminal.

Never place API keys or instance credentials in GitHub commits, screenshots, or shared configuration files.

## 14.8 Hardware Measurement Score

The hardware score is calculated from the measurement counts.

For each measured three-bit string, the system counts the number of `1` bits.

The weighted average is scaled to a score between 0 and 100.

Conceptually:

```text
Hardware Score =
100 × Average Fraction of Measured 1 Bits
```

This score is compared with the corresponding local simulation score.

Differences may arise from finite measurement sampling and hardware noise.

---

# 15. Recorded IBM Quantum Results

NeuroQ-Flood successfully executed two recorded circuit-level experiments on IBM Quantum hardware.

Both used:

```text
Backend: ibm_fez
Shots: 1024
```

## Experiment 1

```text
Job ID:
dbvli22nj2vs73dcpmq0

Local quantum score:
35.1123

IBM hardware score:
32.8776

Absolute difference:
2.2347
```

## Experiment 2

```text
Job ID:
dbvmg85hdvas73bib7bg

Local quantum score:
30.6464

IBM hardware score:
31.3477

Absolute difference:
0.7012
```

## Interpretation

These experiments demonstrate that the project's three-qubit circuit can be executed on real IBM Quantum hardware.

They also allow comparison between local simulation and physical hardware measurements.

However:

- The hardware experiments do not execute the complete forecasting pipeline.
- Hardware scores are not river discharge forecasts.
- The experiments do not establish improved forecasting accuracy.
- The experiments do not demonstrate quantum computational advantage.

---

# 16. Automated Testing

NeuroQ-Flood includes automated tests covering forecasting, adaptive learning, data handling, and quantum integration.

## 16.1 Install pytest

If pytest is not installed:

```bash
python -m pip install pytest==9.2.0
```

## 16.2 Run the Complete Test Suite

From the project root:

```bash
python -m pytest tests/ -v
```

## 16.3 Recorded Test Results

The final recorded test run produced:

```text
33 passed
0 failed
```

The tests include coverage for:

- Adaptive learning
- Forecasting pipeline
- Historical replay
- Data leakage prevention
- Training normalization
- Quantum circuit construction
- Local simulation and Qiskit consistency
- Quantum measurement scoring
- Mocked IBM Quantum hardware execution

## 16.4 Run Individual Test Modules

Adaptive learning:

```bash
python -m pytest tests/test_adaptive_learning.py -v
```

Data leakage:

```bash
python -m pytest tests/test_data_leakage.py -v
```

Forecasting pipeline:

```bash
python -m pytest tests/test_pipeline.py -v
```

IBM Quantum integration:

```bash
python -m pytest tests/test_ibm_quantum.py -v
```

The IBM Quantum integration tests use mocked hardware interactions for relevant scenarios.

Running the automated test suite does not require submitting actual IBM Quantum hardware jobs.

---

# 17. IL-KAN Research Comparison

NeuroQ-Flood was also discussed in relation to published IL-KAN research.

IL-KAN investigates incremental learning using Kolmogorov-Arnold Networks in a hydrological modeling context.

The comparison is intended to provide research context, not to establish a universal ranking between the two approaches.

## 17.1 Within-Study Improvement

| Research System | Reported RMSE Improvement |
|---|---:|
| NeuroQ-Flood | 56.4% |
| IL-KAN | 33.39% |

The NeuroQ-Flood percentage represents improvement relative to its fixed-weight hybrid baseline during the selected July 2024 evaluation.

The IL-KAN percentage represents improvement relative to the baseline used in its published study.

## 17.2 Why These Results Are Not Directly Comparable

The studies use different:

- Hydrological datasets
- Research objectives
- Baseline methods
- Model architectures
- Environmental conditions
- Evaluation procedures

NeuroQ-Flood focuses on 60-minute discharge forecasting for Buffalo Bayou.

The IL-KAN study addresses a different hydrological modeling problem.

Therefore, comparing 56.4% and 33.39% does not demonstrate that NeuroQ-Flood is more accurate than IL-KAN.

## 17.3 Potential Architectural Distinctions

NeuroQ-Flood includes:

- Adaptive quantum encoding
- Feedback-driven weight updates
- Bounded parameter adjustments
- Quantum-derived forecasting features
- Live forecast verification
- Optional real quantum hardware execution

These are architectural characteristics, not experimentally established advantages over IL-KAN.

## 17.4 Research Reference

Chi et al.

*Expert Systems With Applications*, Volume 319, 2026, Article 132098.

DOI:

```text
10.1016/j.eswa.2026.132098
```

See also:

```text
docs/WEEK11_ILKAN_COMPARISON.md
```

Note that the Week 11 document contains earlier preliminary comparison notes. The final comparison should be interpreted using the verified within-study baselines and limitations described above.

---

# 18. Final Presentation Demonstration

The project includes a demonstration script:

```text
evaluation/final_demo.py
```

This script displays the previously recorded project results in an organized terminal presentation.

Run:

```bash
python -m evaluation.final_demo
```

The demonstration includes:

1. Project overview
2. Implemented capabilities
3. Historical forecasting accuracy
4. Adaptive learning
5. Verified live forecasting
6. IBM Quantum hardware experiments
7. Automated testing
8. Final research conclusions

**Important:** This script displays recorded results.

It does not:

- Download new USGS observations
- Generate new forecasts
- Modify adaptive weights
- Submit IBM Quantum jobs
- Recalculate historical experiments

For independent verification, run the actual historical forecasting and testing commands described in this README.

---

# 19. Complete Start-to-Finish Walkthrough

This section provides a complete walkthrough for someone running NeuroQ-Flood for the first time.

The commands should be executed from the project root unless otherwise specified.

## Phase 1 — Install the Project

### Step 1: Clone the Repository

```bash
git clone git clone https://github.com/luvgabe/NeuroQ-FloodL
```

### Step 2: Open the Project

Navigate to the directory containing:

```text
NeuroQFlood.py
```

### Step 3: Create a Virtual Environment

```bash
python3 -m venv .venv
```

### Step 4: Activate the Environment

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 6: Install pytest

```bash
python -m pip install pytest==9.2.0
```

---

## Phase 2 — Verify the Installation

### Step 7: Check the Application

```bash
python NeuroQFlood.py --help
```

Expected result:

The terminal displays the available command-line options.

### Step 8: Run Automated Tests

```bash
python -m pytest tests/ -v
```

Expected result:

The tests execute and report their pass/fail status.

The project's previously recorded final test run passed all 33 tests.

---

## Phase 3 — Run Historical Forecasting

### Step 9: Run the Default Experiment

```bash
python NeuroQFlood.py
```

Expected result:

The system evaluates four forecasting approaches and displays their accuracy metrics.

### Step 10: Run the July 2024 Experiment

```bash
python NeuroQFlood.py --start 2024-07-07 --end 2024-07-10
```

Expected result:

The system processes the July 2024 dataset and prints the historical comparison.

The recorded evaluation achieved:

```text
Adaptive Hybrid MAE:  76.13 cfs
Adaptive Hybrid RMSE: 111.79 cfs
Adaptive Hybrid NSE:  0.9707
```

### Step 11: Examine the Results

Open:

```text
data/results/usgs_08074000_2024-07-07_2024-07-10_adaptive_comparison.csv
```

The CSV contains detailed predictions, observations, and adaptive weight values.

---

## Phase 4 — Demonstrate Live Forecasting

### Step 12: Run a Live Forecast

```bash
python NeuroQFlood.py --live
```

Expected result:

The system retrieves recent USGS observations and attempts to generate a 60-minute forecast.

The result depends on current data availability.

### Step 13: Verify a Completed Forecast

After the target observation becomes available, execute:

```bash
python NeuroQFlood.py --live
```

Expected result:

If a previously issued forecast can be verified, the application reports its prediction error.

Eligible completed forecasts may also trigger adaptive learning.

---

## Phase 5 — Display the Final Research Results

### Step 14: Run the Presentation Script

```bash
python -m evaluation.final_demo
```

Expected result:

The terminal displays the recorded historical, live, adaptive, IBM Quantum, and testing results.

This is the safest way to demonstrate the complete research outcome without submitting new hardware jobs.

---

## Phase 6 — Optional IBM Quantum Hardware Execution

This phase is optional.

It requires valid IBM Quantum credentials and available hardware access.

### Step 15: Start the Hardware Comparison

```bash
python NeuroQFlood.py --ibm-quantum
```

### Step 16: Review the Local Simulation

The application displays the local quantum score and circuit configuration.

### Step 17: Confirm Hardware Submission

When prompted:

```text
Submit this experiment to IBM hardware? (yes/no):
```

Enter `yes` only if you intend to submit a hardware job.

### Step 18: Authenticate

Enter your:

```text
IBM Quantum API key
IBM Quantum instance CRN
```

### Step 19: Review the Results

After the job completes, the terminal displays:

```text
IBM Quantum job ID
Measurement counts
Local quantum score
Hardware quantum score
Absolute difference
```

This completes the optional circuit-level hardware comparison.

---

# 20. Suggested Demonstration Script

The following narration can accompany a live technical demonstration.

## Introduction

"NeuroQ-Flood is an adaptive quantum-hybrid forecasting system designed to predict river discharge 60 minutes into the future.

Our system uses real USGS observations from Buffalo Bayou in Houston, Texas.

We developed the project to investigate whether quantum-derived features and neuroplasticity-inspired adaptive learning could improve forecasting performance."

## Architecture

"The system processes hydrological observations, extracts classical forecasting features, and encodes selected measurements into a three-qubit quantum representation.

The quantum-derived score is combined with classical regression.

We compare persistence, classical regression, fixed quantum-hybrid forecasting, and adaptive quantum-hybrid forecasting."

## Historical Evaluation

"Our historical experiments use chronological training and evaluation.

During the July 2024 experiment, the adaptive hybrid achieved an RMSE of 111.79 cubic feet per second.

That was approximately 32.61% lower than classical regression and 56.4% lower than the fixed quantum hybrid during that selected period."

## Adaptive Learning

"The adaptive model begins with the same regression coefficients as the fixed hybrid.

The difference is that it can update three quantum encoding weights based on completed forecast errors.

During our July 2024 replay, the system accepted 104 adaptive updates."

## Live Forecasting

"We also implemented live USGS data retrieval and automatic forecast verification.

Once a forecast's target observation becomes available, the system can calculate its error and use eligible completed forecasts to update its encoding weights.

We verified this process using a live forecast on November 19, 2026."

## IBM Quantum

"We implemented optional execution on real IBM Quantum hardware.

Two experiments were successfully completed on the ibm_fez processor.

These experiments validate the circuit-level implementation, although normal forecasting still uses local quantum simulation."

## Testing

"Finally, we developed automated tests covering the forecasting pipeline, adaptive learning, data leakage prevention, and quantum integration.

Our final recorded test run passed all 33 tests."

## Conclusion

"Our results demonstrate a functioning adaptive quantum-hybrid forecasting prototype.

The adaptive model showed promising improvements during selected historical evaluations, but performance varied across datasets.

We do not claim universal superiority over classical models or a proven quantum computational advantage."

---

# 21. Troubleshooting

## 21.1 ModuleNotFoundError: neuroq

If a script inside `evaluation/` cannot import `neuroq`, ensure you are running commands from the project root.

For scripts that support module execution, use:

```bash
python -m evaluation.final_demo
```

The historical replay module defines a reusable function and is normally invoked through the main application.

Use:

```bash
python NeuroQFlood.py
```

instead of attempting to execute `evaluation/historical_replay.py` directly.

## 21.2 pytest Is Not Installed

Install pytest:

```bash
python -m pip install pytest==9.2.0
```

Then run:

```bash
python -m pytest tests/ -v
```

## 21.3 Qiskit Import Errors

Verify that the virtual environment is activated.

Reinstall the project dependencies:

```bash
python -m pip install -r requirements.txt
```

## 21.4 USGS Data Is Unavailable

Historical and live forecasting depend on USGS observations.

If live observations are unavailable or outdated, try again later.

For historical experiments, use the included cached datasets when possible.

## 21.5 IBM Quantum Authentication Fails

Check:

- API key validity
- Instance CRN
- IBM Quantum account access
- Backend availability
- Available Runtime Units

Do not place credentials directly in source code.

## 21.6 IBM Backend Is Unavailable

The default backend is:

```text
ibm_fez
```

If it is unavailable, select another backend accessible through your IBM Quantum account:

```bash
python NeuroQFlood.py --ibm-quantum --backend <BACKEND_NAME>
```

## 21.7 Results Differ from Recorded Experiments

Possible causes include:

- Different input data
- Refreshed USGS observations
- Different initial weights
- Different software versions
- Different evaluation periods
- Different live adaptive state
- Quantum hardware sampling noise

Recorded results are specific to their original experimental conditions.

---

# 22. Research Limitations

NeuroQ-Flood is a research prototype.

Several limitations remain.

## 22.1 Limited Geographic Scope

The implementation focuses on USGS station 08074000.

Results may not generalize to other watersheds.

## 22.2 Limited Evaluation Periods

Historical performance was evaluated over selected periods.

A broader evaluation would be needed to establish general reliability.

## 22.3 Variable Model Performance

Adaptive quantum-hybrid forecasting did not outperform every baseline in every historical experiment.

## 22.4 No Demonstrated Quantum Advantage

The project does not establish that quantum computation is faster or more accurate than classical alternatives.

## 22.5 Separate Hardware Validation

IBM Quantum hardware execution validates the circuit separately from the complete forecasting pipeline.

## 22.6 Experimental Risk Classification

The project's risk thresholds have not been historically calibrated for operational flood warning use.

## 22.7 Live Data Dependence

Live forecasting depends on timely USGS observations.

Missing or delayed measurements can prevent forecast generation or verification.

---

# 23. Future Research

Potential future extensions include:

- Additional USGS monitoring stations
- Larger historical datasets
- More diverse flood events
- Rainfall and weather integration
- Soil saturation measurements
- Improved adaptive optimization
- Additional forecasting baselines
- Cross-watershed evaluation
- Longer forecasting horizons
- Expanded hardware experimentation
- Automated scheduled forecasting
- Visualization dashboards
- Better uncertainty estimation
- Operationally calibrated flood-risk thresholds

These are potential future research directions, not features claimed to be implemented in the current version.

---

# 24. Contributors

**NeuroQ-Flood**

Fall 2026 University Research Project

Developed by:

- Gabriel Granados
- Alberto Gonzalez

Research areas:

- Artificial Intelligence
- Quantum Computing
- Adaptive Learning
- Hydrological Forecasting
- Software Engineering

---

# 25. Acknowledgments

The project uses publicly available hydrological observations from the United States Geological Survey.

IBM Quantum hardware was used for optional circuit-level experimentation.

The project also draws research context from published work on incremental learning and hydrological modeling, including IL-KAN.

---

# 26. Final Research Summary

NeuroQ-Flood demonstrates the integration of:

```text
REAL-WORLD HYDROLOGICAL DATA
             +
CLASSICAL REGRESSION
             +
QUANTUM-DERIVED FEATURES
             +
ADAPTIVE LEARNING
             +
FORECAST VERIFICATION
             +
OPTIONAL QUANTUM HARDWARE VALIDATION
```

The completed system supports historical evaluation, live forecasting, adaptive learning, quantum circuit experimentation, and automated testing.

During the selected July 2024 historical evaluation, the adaptive hybrid achieved:

```text
MAE:  76.13 cfs
RMSE: 111.79 cfs
NSE:  0.9707
```

The adaptive hybrid reduced RMSE by approximately 32.61% relative to classical regression during that period.

The project also demonstrated:

```text
104 accepted historical adaptive updates

One verified live forecast with 2.48% error

Two successful IBM Quantum hardware experiments

33 passing automated tests
```

These findings support further investigation of adaptive quantum-hybrid forecasting.

They do not establish universal model superiority or quantum computational advantage.

---

# Disclaimer

**NeuroQ-Flood is an experimental educational research system.**

It does not provide official flood warnings.

It must not be used for emergency response, evacuation planning, infrastructure protection, or public-safety decisions.

Forecasting outputs are experimental and may be inaccurate.

Official flood warnings and emergency information should be obtained from appropriate government and emergency-management authorities.

---

**NeuroQ-Flood — Adaptive Quantum-Hybrid Flood Forecasting**

*Gabriel Granados & Alberto Gonzalez — Fall 2026*