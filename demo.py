"""Run one synthetic falling and one synthetic non-falling scenario."""
from safestepsocks.io import read_trials
from safestepsocks.detection import FallDetector


def main():
    trials = read_trials("data/synthetic_trials.csv")
    for trial_id in ("fall_01", "walk_01"):
        is_fall, samples = trials[trial_id]
        detector = FallDetector()
        alerts = [a for s in samples if (a := detector.process(s)) is not None]
        print(f"{trial_id}: synthetic_fall_label={is_fall}, alerts={len(alerts)}")
        for a in alerts:
            print(f"  [DEMO ONLY] {a.reason} at {a.timestamp_ms} ms")
    print("Synthetic output is NOT a real-world performance measurement.")


if __name__ == "__main__":
    main()
