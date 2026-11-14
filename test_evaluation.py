import tempfile
import unittest
from pathlib import Path
from safestepsocks.detection import MotionSample
from safestepsocks.evaluation import EvaluationResult, evaluate_trials
from safestepsocks.io import read_trials


def m(t, accel, gyro=2):
    return MotionSample(t, 0, 0, accel, gyro, 0, 0)


class EvaluationTests(unittest.TestCase):
    def test_counts_at_trial_level(self):
        fall = [m(0, 0.2), m(100, 3)] + [m(t, 1) for t in range(200, 1600, 100)]
        safe = [m(t, 1.1) for t in range(0, 1600, 100)]
        report = evaluate_trials({"a": (True, fall), "b": (False, safe), "c": (True, safe)})
        self.assertEqual((report.true_positive, report.false_positive, report.true_negative, report.false_negative), (1, 0, 1, 1))
        self.assertEqual(report.sensitivity, 0.5)
        self.assertEqual(report.false_alarm_rate, 0)

    def test_zero_denominator(self):
        result = EvaluationResult(1, 0, 0, 0)
        self.assertIsNone(result.false_alarm_rate)

    def test_csv_rejects_conflicting_labels(self):
        header = "trial_id,timestamp_ms,ax_g,ay_g,az_g,gx_dps,gy_dps,gz_dps,ground_truth_fall\n"
        row1 = "abc,0,0,0,1,0,0,0,1\n"
        row2 = "abc,100,0,0,1,0,0,0,0\n"
        with tempfile.TemporaryDirectory() as temp:
            csv_path = Path(temp) / "trials.csv"
            csv_path.write_text(header + row1 + row2, encoding="utf-8")
            with self.assertRaises(ValueError):
                read_trials(csv_path)


if __name__ == "__main__":
    unittest.main()
