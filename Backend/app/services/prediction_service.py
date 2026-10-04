from sqlalchemy.orm import Session

from app.models.prediction import Prediction
from app.schemas.prediction import PredictionCreate


def create_prediction(db: Session, data: PredictionCreate):
    prediction = Prediction(**data.model_dump())

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction


def get_prediction(db: Session, prediction_id: int):
    return (
        db.query(Prediction)
        .filter(Prediction.id == prediction_id)
        .first()
    )


def get_predictions(db: Session):
    return db.query(Prediction).all()