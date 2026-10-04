import numpy as np


SELECTED_SENSORS = [
    "phase_current_1",
    "phase_current_2",
    "vibration_1"
]

WINDOW_SIZE = 4096


def clean_sensor_data(sensor_data):
    cleaned = {}

    for sensor, data in sensor_data.items():
        data = np.asarray(data, dtype=np.float32).squeeze()

        if not np.all(np.isfinite(data)):
            raise ValueError(
                f"Invalid NaN/Inf values in {sensor} data."
            )

        cleaned[sensor] = data

    return cleaned


def preprocess_sensors(sensor_data, scalers):
    processed = {}

    for sensor in SELECTED_SENSORS:
        data = np.asarray(
            sensor_data[sensor],
            dtype=np.float32
        )

        processed[sensor] = scalers[sensor].transform(
            data.reshape(-1, 1)
        ).squeeze().astype(np.float32)

    return processed


def create_windows(sensor_data):
    lengths = [
        len(sensor_data[sensor])
        for sensor in SELECTED_SENSORS
    ]

    if len(set(lengths)) != 1:
        raise ValueError("Sensor data lengths do not match.")

    num_windows = lengths[0] // WINDOW_SIZE

    windows = []

    for i in range(num_windows):
        start = i * WINDOW_SIZE
        end = start + WINDOW_SIZE

        window = np.stack(
            [
                sensor_data[sensor][start:end]
                for sensor in SELECTED_SENSORS
            ],
            axis=1
        )

        windows.append(window)

    return np.asarray(windows, dtype=np.float32)