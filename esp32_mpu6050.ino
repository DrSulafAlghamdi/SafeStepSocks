/* SafeStepSocks experimental IMU serial streamer.
 * Hardware: ESP32 development board + MPU6050 breakout (3.3 V logic).
 * Libraries: Adafruit MPU6050, Adafruit Unified Sensor, Adafruit BusIO.
 * Output: timestamp_ms,ax_g,ay_g,az_g,gx_dps,gy_dps,gz_dps
 * NOTE: Not a fall-detection medical device or safety-critical product.
 */
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 imu;
const float GRAVITY = 9.80665f;
const float RAD_TO_DEG_F = 57.295779513f;

void setup() {
  Serial.begin(115200);
  delay(1000);
  // These are common ESP32 dev-board I2C pins; verify your exact board.
  Wire.begin(21, 22);
  if (!imu.begin()) {
    Serial.println("IMU not found; verify wiring and power");
    while (true) delay(500);
  }
  imu.setAccelerometerRange(MPU6050_RANGE_8_G);
  imu.setGyroRange(MPU6050_RANGE_500_DEG);
  imu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.println("timestamp_ms,ax_g,ay_g,az_g,gx_dps,gy_dps,gz_dps");
}

void loop() {
  sensors_event_t a, g, temp;
  imu.getEvent(&a, &g, &temp);
  Serial.print(millis()); Serial.print(',');
  Serial.print(a.acceleration.x / GRAVITY, 4); Serial.print(',');
  Serial.print(a.acceleration.y / GRAVITY, 4); Serial.print(',');
  Serial.print(a.acceleration.z / GRAVITY, 4); Serial.print(',');
  Serial.print(g.gyro.x * RAD_TO_DEG_F, 3); Serial.print(',');
  Serial.print(g.gyro.y * RAD_TO_DEG_F, 3); Serial.print(',');
  Serial.println(g.gyro.z * RAD_TO_DEG_F, 3);
  delay(50); // ~20 Hz sample-rate demonstration; tune after empirical study.
}
