import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .ml_model.features import extract_features
from .ml_model.ranker import rank_routes

def clean(obj):
    import numpy as np
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean(v) for v in obj]
    elif isinstance(obj, (np.float32, np.float64, np.int32, np.int64)):
        return float(obj)
    elif hasattr(obj, "item"):
        return obj.item()
    else:
        return obj

@csrf_exempt
def map_input(request):
    
    ranked_routes = None
    features_list = None
    error = None

    if request.method == "POST":
        start_lat = request.POST.get("start_lat")
        start_lng = request.POST.get("start_lng")
        dest_lat = request.POST.get("dest_lat")
        dest_lng = request.POST.get("dest_lng")

        if not start_lat or not start_lng or not dest_lat or not dest_lng:
            error = "Select both start and destination."
        else:
            start = (float(start_lat), float(start_lng))
            dest = (float(dest_lat), float(dest_lng))

            features_list = [clean(f) for f in extract_features(start, dest)]
            if not features_list:
                error = "No routes returned from ORS."
            else:
                ranked_routes = [(int(idx), float(score)) for idx, score in rank_routes(features_list)]

    return render(request, "routing/map_input.html", {
        "ranked_routes": ranked_routes,
        "features_list": features_list,
        "error": error
    })
