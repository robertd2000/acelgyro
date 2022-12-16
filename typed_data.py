from typing import NamedTuple


class SensorData(NamedTuple):
    accel_x: list[float]
    accel_y: list[float]
    accel_z: list[float]
    gyro_x: list[float]
    gyro_y: list[float]
    gyro_z: list[float]
    time: list[float]
    alpha: list[float]
    beta: list[float]
    gamma: list[float]
    angle: list[float]


class VectorData(NamedTuple):
    Ax: list[list[float]]
    Ay: list[list[float]]
    Az: list[list[float]]
