"""Read USB serial IMU telemetry and print LOCAL, NON-EMERGENCY test alerts.

Optional dependency: pip install pyserial
This file does not notify emergency services or caregivers.
"""
import argparse
from safestepsocks.detection import FallDetector, MotionSample


def main():
    parser = argparse.ArgumentParser(description="Local IMU console monitor (not for safety use)")
    parser.add_argument("--port", required=True, help="Serial device, e.g. /dev/ttyUSB0 or COM3")
    parser.add_argument("--baud", type=int, default=115200)
    args = parser.parse_args()
    try:
        import serial
    except ImportError:
        parser.error("Install optional dependency: python -m pip install pyserial")
    detector = FallDetector()
    print("TEST MODE ONLY. No emergency or caregiver messages will be sent.")
    with serial.Serial(args.port, args.baud, timeout=2) as connection:
        while True:
            line = connection.readline().decode("utf-8", errors="replace").strip()
            if not line or line.startswith("timestamp_ms"):
                continue
            try:
                v = line.split(",")
                if len(v) != 7:
                    continue
                sample = MotionSample(int(v[0]), *map(float, v[1:]))
                alert = detector.process(sample)
                if alert:
                    print(f"[EXPERIMENTAL ALERT] at {alert.timestamp_ms}ms — {alert.reason}")
            except ValueError:
                # Boot banners and malformed sample lines are not sensor data.
                continue


if __name__ == "__main__":
    main()
