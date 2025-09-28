from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime

from .services.blockchain import get_all_tourists, get_tourist

@staff_member_required  # authority only
def blockchain_dashboard(request):
    try:
        ids = get_all_tourists()
        tourists = []
        now_ts = int(datetime.utcnow().timestamp())
        
        for tid in ids:
            t = get_tourist(tid)
            # t = (touristId, name, aadhaarHash, validFrom, validTo, registeredBy)
            valid_from = t[3]
            valid_to = t[4]
            still_valid = valid_from <= now_ts <= valid_to

            tourists.append({
                "touristId": t[0],
                "name": t[1],
                "aadhaarHash": t[2],
                "validFrom": valid_from,
                "validTo": valid_to,
                "registeredBy": t[5],  
                "still_valid": still_valid
            })
    except Exception as e:
        tourists = []
        error = str(e)
    else:
        error = None

    return render(request, "blockchain/blockchain_dashboard.html", {
        "tourists": tourists,
        "error": error
    })


from django.http import JsonResponse
from datetime import datetime
from .services.blockchain import get_tourist

def verify_qr(request, tourist_id):
    try:
        t = get_tourist(tourist_id)
        # t = (touristId, name, aadhaarHash, validFrom, validTo, registeredBy)
        valid_from = t[3]
        valid_to = t[4]
        now_ts = int(datetime.utcnow().timestamp())
        still_valid = valid_from <= now_ts <= valid_to

        data = {
            "touristId": t[0],
            "name": t[1],
            
            "still_valid": still_valid,
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
