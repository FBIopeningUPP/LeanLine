from dataclasses import dataclass

@dataclass
class TelemetryFrame:
    timestamp_ms: int
    accel_x: int
    accel_y: int
    accel_z: int
    gyro_x: int
    gyro_y: int
    gyro_z: int
    latitude: int
    longitude: int
    ground_speed: int
    heading: int
    lead_voltage: int