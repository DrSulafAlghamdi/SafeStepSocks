"""Generate simple synthetic demonstration input, never real test evidence."""
import csv
from pathlib import Path
from safestepsocks.io import FIELDNAMES

OUT = Path(__file__).resolve().parents[1] / "data" / "synthetic_trials.csv"


def motion(t, a, gyro=0.0):
    return (t, 0.0, 0.0, a, gyro, 0.0, 0.0)


def make_trial(is_fall, kind="walk"):
    rows = []
    # A benign motion sequence with more vigorous but not freefall-like periods.
    for k in range(15):
        a = (1.15 if k % 4 else 1.7) if kind != "sit" else 1.0
        rows.append(motion(k * 100, a, 35.0 if kind != "sit" else 4.0))
    if is_fall:
        rows.append(motion(1500, 0.2, 70))
        rows.append(motion(1600, 2.8, 120))
        for k in range(17):
            rows.append(motion(1700 + k * 100, 1.0, 2.0))
    else:
        for k in range(17):
            rows.append(motion(1500 + k * 100, 1.1 if k % 3 else 1.0, 18.0))
    return rows


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(FIELDNAMES)
        trial_specs = [(f"fall_{i:02d}", True, "walk") for i in range(1, 5)]
        trial_specs += [(f"walk_{i:02d}", False, "walk") for i in range(1, 7)]
        trial_specs += [(f"sit_{i:02d}", False, "sit") for i in range(1, 3)]
        for trial_id, label, kind in trial_specs:
            for t, ax, ay, az, gx, gy, gz in make_trial(label, kind):
                writer.writerow([trial_id, t, ax, ay, az, gx, gy, gz, int(label)])
    print(f"Wrote {len(trial_specs)} SYNTHETIC trials to {OUT}")
    print("DO NOT quote these example results as product validation.")


if __name__ == "__main__":
    main()
