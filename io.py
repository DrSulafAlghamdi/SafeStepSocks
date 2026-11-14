"""Read reproducible labeled trial CSVs. No participant identifiers needed."""
import csv
from collections import defaultdict
from pathlib import Path
from .detection import MotionSample

FIELDNAMES = [
    "trial_id", "timestamp_ms", "ax_g", "ay_g", "az_g",
    "gx_dps", "gy_dps", "gz_dps", "ground_truth_fall"
]


def read_trials(path: str | Path):
    trials = defaultdict(list)
    labels = {}
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if not set(FIELDNAMES).issubset(reader.fieldnames or []):
            raise ValueError(f"expected columns: {', '.join(FIELDNAMES)}")
        for line_number, row in enumerate(reader, 2):
            trial_id = row["trial_id"].strip()
            if not trial_id:
                raise ValueError(f"missing trial_id at line {line_number}")
            if row["ground_truth_fall"] not in ("0", "1"):
                raise ValueError(f"label must be 0 or 1 at line {line_number}")
            label = row["ground_truth_fall"] == "1"
            if trial_id in labels and labels[trial_id] != label:
                raise ValueError(f"inconsistent label for trial {trial_id}")
            labels[trial_id] = label
            try:
                sample = MotionSample(
                    timestamp_ms=int(row["timestamp_ms"]),
                    ax_g=float(row["ax_g"]), ay_g=float(row["ay_g"]),
                    az_g=float(row["az_g"]), gx_dps=float(row["gx_dps"]),
                    gy_dps=float(row["gy_dps"]), gz_dps=float(row["gz_dps"]),
                )
            except (ValueError, TypeError) as e:
                raise ValueError(f"invalid motion record at line {line_number}") from e
            trials[trial_id].append(sample)
    if not trials:
        raise ValueError("CSV contains no trials")
    return {trial_id: (labels[trial_id], samples) for trial_id, samples in trials.items()}
