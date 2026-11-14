# Testing and data-validation plan

## Claims discipline

The team has **reported** preliminary evaluation involving 50 adults age 40+ and an iterative development result of **2% false alarms**. The raw testing records, population details, protocol, confidence intervals, and denominator were not provided when this repository was prepared; therefore **neither figure is independently substantiated here**. Do not attribute those metrics to the sample detector or synthetic CSV in this repository.

## Suggested evaluation phases

1. **Bench engineering:** sample rates, sensor orientation, calibration drift, power consumption, radio/USB loss and temperature.
2. **Textile:** wet/dry surface traction, repeated washing, textile aging, comfort, heat, and fit for different feet.
3. **Safe simulated activities:** walking, standing up, sitting, stairs, running, dropping a removable instrumented module (NOT a worn sock), and carefully supervised risk-assessed simulation by appropriate volunteers.
4. **Independent performance:** collect labeled trials, hold out participants and scenarios for testing, report confidence intervals and subgroups; obtain ethics review when applicable.
5. **Real-world usability:** observational comfort/wearability tests, connectivity uptime and false alarms per person-hour. Any monitoring that affects clinical care needs appropriate oversight and validation.

**Never deliberately induce falls in at-risk participants.** The code cannot guarantee fall detection.

## Metrics to report separately

- **Sensitivity:** TP / (TP + FN), proportion of true fall trials alerted.
- **Specificity:** TN / (TN + FP), proportion of non-fall trials not alerted.
- **False-alarm rate per non-fall trial:** FP / (FP + TN). This is the definition used by `scripts/evaluate_csv.py`.
- **False alerts per wearing hour:** raw alert count across negative exposure hours, another useful metric that is NOT automatically comparable to per-trial percentages.
- **Precision:** TP / (TP + FP). Depends heavily on prevalence in test data.
- **End-to-end notification latency:** event to receipt and acknowledgment, when a real mobile system exists.
- **Slip resistance:** standardized traction measurements (separate from detection).
- **User acceptance:** structured measures and consented de-identified interview findings.

A statement like **'2% false alarms'** is incomplete unless the denominator, study size, setting, firmware/algorithm version, confidence interval and failure cases are documented. **2% false-alarm rate does not mean 98% fall-detection sensitivity or accuracy.**

## Data schema for offline trial CSV

| Column | Meaning |
| --- | --- |
| `trial_id` | Pseudonymous independent trial identifier |
| `timestamp_ms` | Strictly increasing timestamp within a trial |
| `ax_g, ay_g, az_g` | Linear accelerometer readings expressed in g including gravity |
| `gx_dps, gy_dps, gz_dps` | Angular velocity in degrees/s |
| `ground_truth_fall` | 1 = labeled fall trial; 0 = labeled non-fall trial |

Keep a separate, access-restricted source record identifying how each event was labeled, consent and collection conditions. Do **not** commit identifying information or participant-level sensitive data to GitHub. The checked-in `data/synthetic_trials.csv` is demonstrative only.

## Suggested result report fields

`protocol`, `version`, `dates`, `ethics_approval_or_exemption`, `participants`, `trials`, `exposure_hours`, `fall_definition`, `TP`, `FP`, `TN`, `FN`, `false_alerts_per_hour`, `sensitivity`, `specificity`, `uncertainty`, `device_failure_count`, `notification_latency`, `limitations`.
