import unittest
from safestepsocks.detection import DetectorConfig, FallDetector, MotionSample


def m(t, accel, gyro=2):
    return MotionSample(t, 0, 0, accel, gyro, 0, 0)


class FallDetectorTests(unittest.TestCase):
    def test_possible_fall_generates_one_alert(self):
        samples = [m(0, 1), m(100, 0.2, 60), m(200, 3.1, 120)]
        samples += [m(t, 1) for t in range(300, 1800, 100)]
        detector = FallDetector()
        alerts = [a for s in samples if (a := detector.process(s))]
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].impact_timestamp_ms, 200)

    def test_impact_without_low_g_not_detected(self):
        detector = FallDetector()
        self.assertFalse(any(detector.process(m(i * 100, a)) for i, a in enumerate([1, 2.8, 1, 1, 1])))

    def test_no_stillness_no_alert(self):
        detector = FallDetector()
        samples = [m(0, 0.2), m(100, 3.0)] + [m(t, 1, 90) for t in range(200, 4100, 100)]
        self.assertFalse(any(detector.process(s) for s in samples))

    def test_stale_freefall_expires(self):
        detector = FallDetector()
        samples = [m(0, 0.2), m(1200, 3.1)] + [m(t, 1) for t in range(1300, 2900, 100)]
        self.assertFalse(any(detector.process(s) for s in samples))

    def test_duplicate_timestamp_rejected(self):
        detector = FallDetector()
        detector.process(m(100, 1))
        with self.assertRaises(ValueError):
            detector.process(m(100, 1))

    def test_bad_config_rejected(self):
        with self.assertRaises(ValueError):
            DetectorConfig(freefall_g=1.1)


if __name__ == "__main__":
    unittest.main()
