import numpy as np
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

model = joblib.load(MODEL_PATH)

FEATURE_ORDER = [
    "distance_m",
    "duration_s",
    "duration_in_traffic_s",
    "elevation_gain_m",
    "sinuosity",
    "num_turns",
    "turn_complexity_score",
    "avg_segment_length_m",
    "num_zone_intersections",
    "total_unsafe_length_m",
    "unsafe_fraction",
    "max_zone_risk",
    "traffic_level",
    "weather_penalty",
    "time_of_day_bucket",
    "day_of_week",
    "lighting_proxy",
    "poi_density_along_route"
]

def rank_routes(route_features_list):
    if not route_features_list:
        return []

    X = np.array([[f[feat] for feat in FEATURE_ORDER] for f in route_features_list], dtype=float)
    scores = model.predict(X)
    scores = [float(s) for s in scores]
    ranked = sorted(zip(range(len(route_features_list)), scores), key=lambda x: x[1], reverse=True)
    return ranked
