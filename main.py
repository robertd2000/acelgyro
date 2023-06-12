from datetime import datetime as t
import matplotlib.pyplot as plt
import math
import numpy as np
from utils import calculate_angle, transform_data, unix_time_millis, mean, get_standard_vector_matrix
from typed_data import SensorData, VectorData

vector_data = VectorData(Ax=[], Ay=[], Az=[])


def get_data_from_file(filename: str) -> SensorData:
    res = SensorData(accel_x=[], accel_y=[], 
                     accel_z=[], gyro_x=[], 
                     gyro_y=[], gyro_z=[], 
                     time=[], alpha=[], beta=[],
                     gamma=[], angle=[])
    with open(file=filename) as f:
        i = 0
        j = 0
        n = 0
        reset_vector_data()

        for line in f:
            if len(line.split('`')) < 9:
                if j > 0:
                    n += 1
                    reset_vector_data()

                j = 0
                continue

            fill_sensors_data(res, line, i)
            fill_angle_data(res, i)
            fill_vector_data(n, res.accel_x[i], res.accel_y[i], res.accel_z[i])

            i += 1
            j += 1

    return res


def reset_vector_data():
    vector_data.Ax.append([])
    vector_data.Ay.append([])
    vector_data.Az.append([])


def fill_sensors_data(target: SensorData, line: str, i: int = 1):
    (accel_x, accel_y, accel_z, gyro_x,
     gyro_y, gyro_z, *rest, time, _) = line.split('`')
    target.accel_x.append(transform_data(accel_x))
    target.accel_y.append(transform_data(accel_y))
    target.accel_z.append(transform_data(accel_z))
    target.gyro_x.append(transform_data(gyro_x))
    target.gyro_y.append(transform_data(gyro_y))
    target.gyro_z.append(transform_data(gyro_z))
    target.time.append(unix_time_millis(t.fromisoformat(time.replace('/', '-').replace('_', ' '))) + i * 200)


def fill_angle_data(target: SensorData, i: int):
    target.alpha.append(calculate_angle(target.accel_x[i], target.accel_y[i], target.accel_z[i]))
    target.beta.append(calculate_angle(target.accel_y[i], target.accel_x[i], target.accel_z[i]))
    target.gamma.append(calculate_angle(target.accel_z[i], target.accel_x[i], target.accel_y[i]))
    target.angle.append(math.fabs(target.alpha[i]) + math.fabs(target.beta[i]) + math.fabs(target.gamma[i]))


def fill_vector_data(n, x, y, z):
    vector_data.Ax[n].append(x)
    vector_data.Ay[n].append(y)
    vector_data.Az[n].append(z)


def get_coefficient(x: list[float], y: list[float], z: list[float]) -> (float, list[float]):
    k = [90 - max(abs(xi), abs(yi), abs(zi)) for xi, yi, zi in zip(x, y, z)]
    return mean(k), k


def find_position(x: float, y: float, z: float) -> str:
    x, y, z = abs(x), abs(y), abs(z)
    position = ''
    if max(x, y, z) < 0 and z > x and z > y:
        position = 'Позиция 1. Поверните датчик!'
    if max(x, y, z) < 0 and x > y and x > z:
        position = 'Позиция 2. Поверните датчик!'
    if max(x, y, z) < 0 and y > x and y > z:
        position = 'Позиция 3. Поверните датчик!'
    if max(x, y, z) > 0 and x > y and x > z:
        position = 'Позиция 4. Поверните датчик!'
    if max(x, y, z) > 0 and abs(x) > abs(z) and abs(x) > abs(y):
        position = 'Позиция 5. Поверните датчик!'
    if max(x, y, z) > 0 and abs(z) > abs(x) and abs(z) > abs(y):
        position = 'Позиция 6. Датчик расположен вверх ногами. Переверните датчик!'

    return position


def find_positions(x: list[float], y: list[float], z: list[float]):
    return [print(find_position(xi, yi, zi)) for xi, yi, zi in zip(x, y, z)]

def draw(time: list[float], x: list[float], y: list[float], z: list[float], a=None):
    if a is None:
        a = []
    plt.figure(figsize=(12, 7))
    plt.plot(time, x, label='accel_x_mps2 ', c='r')
    plt.plot(time, y, label='accel_y_mps2 ', c='g')
    plt.plot(time, z, label='accel_z_mps2 ', c='b')
    plt.plot(time, a, label='accel_z_mps2 ', c='black')
    plt.legend()
    plt.grid(True)
    plt.show()


def fill_vector_matrix():
    matrix = []
    for i in range(len(vector_data.Ax) - 1):
        matrix.append([0, 0, 0, mean(vector_data.Ax[i]),
                       mean(vector_data.Ay[i]),
                       mean(vector_data.Az[i])])

    return np.array(matrix)


def draw_vector(limit: int = 10):
    soa = fill_vector_matrix()
    sob = get_standard_vector_matrix()

    x1, y1, z1, u1, v1, w1 = zip(*soa)
    x2, y2, z2, u2, v2, w2 = zip(*sob)

    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(x1, y1, z1, u1, v1, w1, color="blue")
    ax.quiver(x2, y2, z2, u2, v2, w2, color="red")

    ax.set_xlim([-limit, limit])
    ax.set_ylim([-limit, limit])
    ax.set_zlim([-limit, limit])
    plt.show()


def scatter_draw(x: list[float], y: list[float]):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.plot(x, y, 'b')
    plt.show()


def main():
    file_data = get_data_from_file('data/data.txt')
    # file_data = get_data_from_file('data/spin_data.txt')
    # draw(file_data.time, file_data.accel_x,  file_data.accel_y, file_data.accel_z)
    draw(file_data.time, file_data.alpha, file_data.beta, file_data.gamma, file_data.angle)
    draw_vector()
    print(get_coefficient(file_data.alpha, file_data.beta, file_data.gamma))
    find_positions(file_data.alpha, file_data.beta, file_data.gamma)
    # scatter_draw(data.accel_x, data.accel_y)
    # scatter_draw(data.gyro_x, data.gyro_y)


if __name__ == '__main__':
    main()
