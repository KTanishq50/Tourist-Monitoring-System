# track/ml_utils/model_io.py
import os
import pickle
from django.conf import settings

def load_model():
    path = os.path.join(settings.BASE_DIR, "track", "ml_model", "ml_model.pkl")
    with open(path, "rb") as f:
        return pickle.load(f)
