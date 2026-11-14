"""Report trial-based metrics, not clinical validation."""
import argparse
import json
from safestepsocks.io import read_trials
from safestepsocks.evaluation import evaluate_trials


def main():
    parser = argparse.ArgumentParser(description="Experimental trial-level evaluator")
    parser.add_argument("file", help="CSV with trial_id, motion columns, ground_truth_fall")
    args = parser.parse_args()
    result = evaluate_trials(read_trials(args.file))
    print(json.dumps(result.as_dict(), indent=2))
    print("Metrics depend on scenario selection and ground-truth quality.")
    print("Synthetic CSV results are NOT human or clinical evidence.")


if __name__ == "__main__":
    main()
