"""Trial-level evaluation; never treat row-level samples as independent falls."""
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence
from .detection import FallDetector, MotionSample


@dataclass(frozen=True)
class EvaluationResult:
    true_positive: int
    false_positive: int
    true_negative: int
    false_negative: int

    @property
    def total_trials(self) -> int:
        return self.true_positive + self.false_positive + self.true_negative + self.false_negative

    @property
    def sensitivity(self):
        d = self.true_positive + self.false_negative
        return self.true_positive / d if d else None

    @property
    def specificity(self):
        d = self.true_negative + self.false_positive
        return self.true_negative / d if d else None

    @property
    def false_alarm_rate(self):
        """Fraction of NON-FALL trials with one or more alerts (not alerts/hour)."""
        d = self.false_positive + self.true_negative
        return self.false_positive / d if d else None

    @property
    def precision(self):
        d = self.true_positive + self.false_positive
        return self.true_positive / d if d else None

    def as_dict(self) -> dict:
        return {
            "unit_of_analysis": "trial",
            "trials": self.total_trials,
            "true_positive": self.true_positive,
            "false_positive": self.false_positive,
            "true_negative": self.true_negative,
            "false_negative": self.false_negative,
            "sensitivity": self.sensitivity,
            "specificity": self.specificity,
            "false_alarm_rate_per_non_fall_trial": self.false_alarm_rate,
            "precision": self.precision,
        }


def evaluate_trials(trials: Mapping[str, tuple[bool, Sequence[MotionSample]]]) -> EvaluationResult:
    tp = fp = tn = fn = 0
    for trial_id, (is_fall, samples) in trials.items():
        if not samples:
            raise ValueError(f"empty trial: {trial_id}")
        detector = FallDetector()  # Reset between independent trials.
        predicted = False
        for sample in samples:
            predicted |= detector.process(sample) is not None
        if is_fall and predicted:
            tp += 1
        elif is_fall and not predicted:
            fn += 1
        elif not is_fall and predicted:
            fp += 1
        else:
            tn += 1
    return EvaluationResult(tp, fp, tn, fn)
