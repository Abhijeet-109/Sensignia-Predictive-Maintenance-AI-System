from app.inference.model_loader import scalers
from app.inference.preprocessing import (
    clean_sensor_data,
    preprocess_sensors,
    create_windows,
)
from app.inference.predictor import predict


def run_inference(sensor_data):
    sensor_data = clean_sensor_data(sensor_data)

    sensor_data = preprocess_sensors(
        sensor_data,
        scalers
    )

    windows = create_windows(sensor_data)

    predictions = predict(windows)

    return predictions