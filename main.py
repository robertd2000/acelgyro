from typing import NamedTuple

import matplotlib.pyplot as plt


class SensorData(NamedTuple):
    accel_x: list[float]
    accel_y: list[float]
    accel_z: list[float]
    gyro_x: list[float]
    gyro_y: list[float]
    gyro_z: list[float]


def get_data_from_file(filename: str) -> SensorData:
    res = SensorData(accel_x=[], accel_y=[], accel_z=[], gyro_x=[], gyro_y=[], gyro_z=[])
    with open(file=filename) as f:
        for line in f:
            if len(line.split('`')) < 9:
                continue
            accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, *rest = line.split('`')
            res.accel_x.append(transform_data(accel_x))
            res.accel_y.append(transform_data(accel_y))
            res.accel_z.append(transform_data(accel_z))
            res.gyro_x.append(transform_data(gyro_x))
            res.gyro_y.append(transform_data(gyro_y))
            res.gyro_z.append(transform_data(gyro_z))

    return res


def transform_data(x: str) -> float:
    try:
        return float(x) / 1000
    except ValueError:
        return 0.0


def draw(data: SensorData):
    plt.figure(figsize=(12, 7))
    plt.plot(data.accel_x, label='accel_x_mps2 ')
    plt.plot(data.accel_y, label='accel_y_mps2 ')
    plt.plot(data.accel_z, label='accel_z_mps2 ')
    # plt.plot(data.gyro_x, label='gyro_x_radps  ')
    # plt.plot(data.gyro_y, label='gyro_y_radps  ')
    # plt.plot(data.gyro_z, label='gyro_z_radps  ') #данные гироскопа линейные
    plt.legend()
    plt.grid(True)
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
    data = get_data_from_file('data/data.txt')
    print(data)
    draw(data)
    scatter_draw(data.accel_x, data.accel_y)
    scatter_draw(data.gyro_x, data.gyro_y)


if __name__ == '__main__':
    main()
