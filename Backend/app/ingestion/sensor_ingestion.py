import numpy as np


SELECTED_SENSORS = [
    "phase_current_1",
    "phase_current_2",
    "vibration_1"
]


def validate_sensor_data(sensor_data):
    for sensor in SELECTED_SENSORS:
        if sensor not in sensor_data:
            raise ValueError(
                f"Missing sensor data: {sensor}"
            )

        data = np.asarray(
            sensor_data[sensor],
            dtype=np.float32
        )

        if data.size == 0:
            raise ValueError(
                f"No data available for sensor: {sensor}"
            )

        if not np.all(np.isfinite(data)):
            raise ValueError(
                f"Invalid NaN/Inf values in {sensor} data."
            )

    lengths = [
        len(sensor_data[sensor])
        for sensor in SELECTED_SENSORS
    ]

    if len(set(lengths)) != 1:
        raise ValueError(
            "All sensor data must have the same length."
        )

    return {
        sensor: np.asarray(
            sensor_data[sensor],
            dtype=np.float32
        )
        for sensor in SELECTED_SENSORS
    }