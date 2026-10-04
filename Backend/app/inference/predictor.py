import numpy as np

from app.inference.model_loader import model, class_mapper


def predict(windows):
    if len(windows) == 0:
        raise ValueError("No valid windows available for prediction.")

    predictions = model.predict(windows, verbose=0)

    results = []

    for prediction in predictions:
        class_id = int(np.argmax(prediction))
        confidence = float(prediction[class_id])

        results.append({
            "predicted_class": class_mapper[class_id],
            "confidence": confidence
        })

    return results