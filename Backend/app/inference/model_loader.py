import os
import pickle

from tensorflow.keras.models import load_model


MODEL_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "models",
        "R55i",
        "Drive_Unit",
        "Electrical_Motor",
        "components",
        "Bearing"
    )
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "sensignia_cnn_lstm.keras"
)

CLASS_MAPPER_PATH = os.path.join(
    MODEL_DIR,
    "class_mapper.pkl"
)

SCALERS_PATH = os.path.join(
    MODEL_DIR,
    "scalers.pkl"
)


model = load_model(MODEL_PATH)

with open(CLASS_MAPPER_PATH, "rb") as f:
    class_mapper = pickle.load(f)

with open(SCALERS_PATH, "rb") as f:
    scalers = pickle.load(f)