import math
from datetime import datetime
import numpy as np

epoch = datetime.utcfromtimestamp(0)
R_T_D = 180.0 / math.pi


def calculate_angle(v1: float, v2: float, v3: float) -> float:
    return math.atan2(v1, math.sqrt(v2 ** 2 + v3 ** 2)) * R_T_D


def unix_time_millis(dt: datetime) -> float:
    return (dt - epoch).total_seconds() * 1000.0


def transform_data(x: str) -> float:
    try:
        return float(x) / 1000
    except ValueError:
        return 0.0


def mean(a: list[float]):
    return np.mean(a)


def get_standard_vector_matrix(limit: int = 10):
    return np.array([
        [0, 0, 0, 0, 0, limit],
        [0, 0, 0, limit, 0, 0],
        [0, 0, 0, 0, limit, 0],
        [0, 0, 0, -limit, 0, 0],
        [0, 0, 0, 0, -limit, 0],
        [0, 0, 0, 0, 0, -limit]
    ])