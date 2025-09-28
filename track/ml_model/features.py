# track/ml_utils/features.py
import numpy as np
from zones.models import Zone
from shapely.geometry import Point, shape

def extract_features(coords, user):
    """
    Convert last N coords into ML feature vector.
    Feature vector order must match training:
    1. mean distance
    2. std distance
    3. safe_count
    4. unsafe_count
    5. restricted_count
    """

    features = []

  
    dists = [np.sqrt((coords[i][0]-coords[i-1][0])**2 + (coords[i][1]-coords[i-1][1])**2)
             for i in range(1, len(coords))]
    features.append(np.mean(dists) if dists else 0)
    features.append(np.std(dists) if dists else 0)

    safe = unsafe = restricted = 0

    for lat, lon in coords:
        point = Point(lon, lat) 
        for z in Zone.objects.all():
            try:
                polygon = shape(z.geom)  
            except Exception:
                continue  
            if polygon.contains(point):
                if z.zone_type == "safe":
                    safe += 1
                elif z.zone_type == "unsafe":
                    unsafe += 1
                elif z.zone_type == "restricted":
                    restricted += 1

    features.extend([safe, unsafe, restricted])
    return features
