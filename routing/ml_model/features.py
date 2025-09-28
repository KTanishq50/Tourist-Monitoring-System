import requests
import numpy as np
from datetime import datetime
from shapely.geometry import LineString, shape
from geopy.distance import geodesic
from django.conf import settings
from zones.models import Zone


def haversine_distance(coord1, coord2):
    return geodesic(coord1, coord2).meters

def decode_polyline(polyline_str):
    import polyline
    return [(lat, lng) for lat, lng in polyline.decode(polyline_str)]

def compute_elevation_gain(coords):
    elevations = []
    for i in range(0, len(coords), 50):
        chunk = coords[i:i+50]
        locs = "|".join([f"{lat},{lng}" for lat, lng in chunk])
        url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={locs}&key={settings.GOOGLE_API_KEY}"
        res = requests.get(url).json()
        elevations += [r["elevation"] for r in res.get("results", [])]

    gain = 0
    for i in range(1, len(elevations)):
        diff = elevations[i] - elevations[i-1]
        if diff > 0:
            gain += diff
    return gain

def compute_turns_and_complexity(coords):
    def angle(p1, p2, p3):
        v1 = np.array([p1[0]-p2[0], p1[1]-p2[1]])
        v2 = np.array([p3[0]-p2[0], p3[1]-p2[1]])
        dot = np.dot(v1, v2)
        norm = np.linalg.norm(v1)*np.linalg.norm(v2)
        return np.arccos(dot/norm) if norm != 0 else 0

    num_turns, complexity = 0, 0
    for i in range(1, len(coords)-1):
        theta = angle(coords[i-1], coords[i], coords[i+1])
        deg = np.degrees(theta)
        if deg < 170:
            num_turns += 1
            complexity += abs(180 - deg)
    return num_turns, complexity

def compute_zone_features(coords):
    line = LineString(coords)
    total_unsafe, max_risk = 0, 0
    zones_crossed = set()
    risk_map = {"safe":0, "restricted":1, "unsafe":2}

    for zone in Zone.objects.all():
        polygon = shape(zone.geom)
        if line.intersects(polygon):
            zones_crossed.add(zone.id)
            intersect_len = line.intersection(polygon).length * 111139
            if zone.zone_type in ["unsafe","restricted"]:
                total_unsafe += intersect_len
            max_risk = max(max_risk, risk_map.get(zone.zone_type,0))
    return len(zones_crossed), total_unsafe, max_risk

def get_weather_penalty(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={settings.OWM_API_KEY}"
    res = requests.get(url).json()
    rain = res.get("rain", {}).get("1h",0)
    wind = res.get("wind", {}).get("speed",0)
    return rain*2 + wind

def get_poi_density(coords):
    density = 0
    for i in range(0, len(coords), 20):
        lat, lng = coords[i]
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=200&key={settings.GOOGLE_API_KEY}"
        res = requests.get(url).json()
        density += len(res.get("results", []))
    return density

def to_native(val):
    import numpy as np
    if isinstance(val, (np.float32,np.float64,np.int32,np.int64)):
        return val.item()
    if isinstance(val, list): return [to_native(x) for x in val]
    if isinstance(val, tuple): return tuple(to_native(x) for x in val)
    if isinstance(val, dict): return {k: to_native(v) for k,v in val.items()}
    return val


def extract_features(start, dest):
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    headers = {
        "Authorization": settings.ORS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "coordinates": [[start[1], start[0]], [dest[1], dest[0]]],
        "alternative_routes": {"target_count":3,"share_factor":0.6,"weight_factor":1.4}
    }

    res = requests.post(url, headers=headers, json=payload).json()
    features_list = []

    routes = res.get("features", [])[:3]
    if not routes:
        print("ORS returned no routes:", res)

    for route in routes:
        coords = [(pt[1], pt[0]) for pt in route["geometry"]["coordinates"]]
        distance_m = route["properties"]["summary"]["distance"]
        duration_s = route["properties"]["summary"]["duration"]

        straight_line = haversine_distance(coords[0], coords[-1])
        sinuosity = distance_m / straight_line if straight_line>0 else 1.0
        num_turns, turn_complexity = compute_turns_and_complexity(coords)
        num_zone_int, unsafe_len, max_risk = compute_zone_features(coords)
        unsafe_fraction = unsafe_len / distance_m if distance_m>0 else 0
        elevation_gain = compute_elevation_gain(coords)
        weather_penalty = get_weather_penalty(coords[0][0], coords[0][1])
        poi_density = get_poi_density(coords)
        avg_segment_length = distance_m / len(coords)
        now = datetime.now()
        time_bucket = now.hour
        day_of_week = now.weekday()
        lighting_proxy = 1 if (time_bucket < 6 or time_bucket > 19) and poi_density < 5 else 0

        features = {
            "distance_m": distance_m,
            "duration_s": duration_s,
            "duration_in_traffic_s": duration_s,
            "elevation_gain_m": elevation_gain,
            "sinuosity": sinuosity,
            "num_turns": num_turns,
            "turn_complexity_score": turn_complexity,
            "avg_segment_length_m": avg_segment_length,
            "num_zone_intersections": num_zone_int,
            "total_unsafe_length_m": unsafe_len,
            "unsafe_fraction": unsafe_fraction,
            "max_zone_risk": max_risk,
            "traffic_level": 1.0,
            "weather_penalty": weather_penalty,
            "time_of_day_bucket": time_bucket,
            "day_of_week": day_of_week,
            "lighting_proxy": lighting_proxy,
            "poi_density_along_route": poi_density,
            "geometry": coords
        }
        features_list.append(to_native(features))

    return features_list
