import numpy as np

from app.ingestion.sensor_ingestion import (
    SELECTED_SENSORS,
    validate_sensor_data,
)


def generate_sensor_data(length=4096):
    sensor_data = {
        "phase_current_1": np.random.normal(0, 1, length),
        "phase_current_2": np.random.normal(0, 1, length),
        "vibration_1": np.random.normal(0, 1, length),
    }

    return validate_sensor_data(sensor_data)