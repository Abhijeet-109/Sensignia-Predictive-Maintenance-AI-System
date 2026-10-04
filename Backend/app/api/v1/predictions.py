from collections import Counter

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.inference.pipeline import run_inference
from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
)
from app.services import prediction_service


router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
)


@router.post("/", response_model=PredictionResponse)
def create_prediction(
    data: PredictionRequest,
    db: Session = Depends(get_db)
):
    sensor_data = {
        "phase_current_1": data.phase_current_1,
        "phase_current_2": data.phase_current_2,
        "vibration_1": data.vibration_1,
    }

    results = run_inference(sensor_data)

    classes = [
        result["predicted_class"]
        for result in results
    ]

    final_class = Counter(classes).most_common(1)[0][0]

    matching_confidences = [
        result["confidence"]
        for result in results
        if result["predicted_class"] == final_class
    ]

    final_confidence = sum(
        matching_confidences
    ) / len(matching_confidences)

    prediction_data = {
        "component_id": data.component_id,
        "model_id": data.model_id,
        "predicted_class": final_class,
        "confidence": final_confidence,
    }

    prediction = prediction_service.create_prediction(
        db,
        prediction_data
    )

    return prediction