from typing import NamedTuple
import datetime
from datetime import datetime as t
import matplotlib.pyplot as plt
import math
import numpy as np

R_T_D = 180.0 / math.pi

epoch = datetime.datetime.utcfromtimestamp(0)


class SensorData(NamedTuple):
    accel_x: list[float]
    accel_y: list[float]
    accel_z: list[float]
    gyro_x: list[float]
    gyro_y: list[float]
    gyro_z: list[float]
    time: list[str]
    alpha: list[float]
    beta: list[float]
    gamma: list[float]
    angle: list[float]


# class Data(NamedTuple):
#     Ax: list[list[float]]
#     Ay: list[list[float]]
#     Az: list[list[float]]


# data = Data(Ax=[], Ay=[], Az=[])
data = {
    'Ax': [],
    'Ay': [],
    'Az': []
}


def get_data_from_file(filename: str) -> SensorData:
    res = SensorData(accel_x=[], accel_y=[], accel_z=[], gyro_x=[], gyro_y=[], gyro_z=[], time=[], alpha=[], beta=[],
                     gamma=[], angle=[])
    with open(file=filename) as f:
        i = 0
        j = 0
        n = 0
        data['Ax'].append([])
        data['Ay'].append([])
        data['Az'].append([])
        for line in f:
            if 'Disconnected' in line:
                # n += 1
                # Data.Ax[n].append(numpy.mean(res.accel_x))
                # Data.Ay[n].append(numpy.mean(res.accel_y))
                # Data.Az[n].append(numpy.mean(res.accel_z))
                continue
            if len(line.split('`')) < 9:
                if j > 0:
                    n += 1
                    data['Ax'].append([])
                    data['Ay'].append([])
                    data['Az'].append([])
                j = 0
                # data['Ax'][n] = []
                # data['Ay'][n] = []
                # data['Az'][n] = []

                continue
            accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, *rest, time, _ = line.split('`')
            res.accel_x.append(transform_data(accel_x))
            res.accel_y.append(transform_data(accel_y))
            res.accel_z.append(transform_data(accel_z))
            res.gyro_x.append(transform_data(gyro_x))
            res.gyro_y.append(transform_data(gyro_y))
            res.gyro_z.append(transform_data(gyro_z))
            # 2022/12/13_14:27:35

            res.time.append(unix_time_millis(t.fromisoformat(time.replace('/', '-').replace('_', ' '))) + i * 200)
            res.alpha.append(math.atan2(res.accel_x[i], math.sqrt(res.accel_y[i] ** 2 + res.accel_z[i] ** 2)) * R_T_D)
            res.beta.append(math.atan2(res.accel_y[i], math.sqrt(res.accel_x[i] ** 2 + res.accel_z[i] ** 2)) * R_T_D)
            res.gamma.append(math.atan2(res.accel_z[i], math.sqrt(res.accel_x[i] ** 2 + res.accel_y[i] ** 2)) * R_T_D)

            res.angle.append(math.fabs(res.alpha[i]) + math.fabs(res.beta[i]) + math.fabs(res.gamma[i]))

            data['Ax'][n].append(res.accel_x[i])  # += res.accel_x[i]
            data['Ay'][n].append(res.accel_y[i])  # += res.accel_y[i]
            data['Az'][n].append(res.accel_z[i])  # += res.accel_z[i]

            i += 1
            j += 1

    return res


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


def transform_data(x: str) -> float:
    try:
        return float(x) / 1000
    except ValueError:
        return 0.0


def draw(time, x, y, z, a=[]):
    plt.figure(figsize=(12, 7))
    plt.plot(time, x, label='accel_x_mps2 ', c='r')
    plt.plot(time, y, label='accel_y_mps2 ', c='g')
    plt.plot(time, z, label='accel_z_mps2 ', c='b')
    plt.plot(time, a, label='accel_z_mps2 ', c='black')

    # plt.plot(data.gyro_x, label='gyro_x_radps  ')
    # plt.plot(data.gyro_y, label='gyro_y_radps  ')
    # plt.plot(data.gyro_z, label='gyro_z_radps  ') #данные гироскопа линейные
    plt.legend()
    plt.grid(True)
    plt.show()


def draw_vector():
    # soa = np.array([[0, 0, 1, 1, -2, 0], [0, 0, 2, 1, 1, 0],
    #             [0, 0, 3, 2, 1, 0], [0, 0, 4, 0.5, 0.7, 0]])

    soa = np.array([
        [0, 0, 0, np.mean(data['Ax'][0]), np.mean(data['Ay'][0]), np.mean(data['Az'][0])],
        [0, 0, 0, np.mean(data['Ax'][1]), np.mean(data['Ay'][1]), np.mean(data['Az'][1])],
        [0, 0, 0, np.mean(data['Ax'][2]), np.mean(data['Ay'][2]), np.mean(data['Az'][2])],
        [0, 0, 0, np.mean(data['Ax'][3]), np.mean(data['Ay'][3]), np.mean(data['Az'][3])],
        [0, 0, 0, np.mean(data['Ax'][4]), np.mean(data['Ay'][4]), np.mean(data['Az'][4])],
        [0, 0, 0, np.mean(data['Ax'][5]), np.mean(data['Ay'][5]), np.mean(data['Az'][5])]
    ])

    sob = np.array([
        [0, 0, 0, 0, 0, 10],
        [0, 0, 0, 10, 0, 0],
        [0, 0, 0, 0, 10, 0],
        [0, 0, 0, -10, 0, 0],
        [0, 0, 0, 0, -10, 0],
        [0, 0, 0, 0, 0, -10]
    ])
    X, Y, Z, U, V, W = zip(*soa)
    X1, Y1, Z1, U1, V1, W1 = zip(*sob)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(X, Y, Z, U, V, W, color="blue")
    ax.quiver(X1, Y1, Z1, U1, V1, W1, color="red")

    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-10, 10])
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
    # draw(file_data.time, file_data.accel_x,  file_data.accel_y, file_data.accel_z)
    draw(file_data.time, file_data.alpha, file_data.beta, file_data.gamma, file_data.angle)
    draw_vector()
    # scatter_draw(data.accel_x, data.accel_y)
    # scatter_draw(data.gyro_x, data.gyro_y)


if __name__ == '__main__':
    main()
