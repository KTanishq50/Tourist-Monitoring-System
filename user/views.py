import os
import uuid
import time
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import TouristProfile
from track.models import UserLocation

try:
    from blockchain.services.blockchain import add_tourist
except Exception:
    add_tourist = None


try:
    import qrcode
except ImportError:
    qrcode = None

def register(request):
    
    if request.user.is_authenticated:
        logout(request)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        aadhaar = request.POST.get("aadhaar")
        pan = request.POST.get("pan")
        days = int(request.POST.get("days", 1))
        
     
        # Government API verification (commented)
      
        
        # verify = call_govt_api(aadhaar, pan)
        # For prototype/demo we assume verified=True
        verified = True
       

        if User.objects.filter(username=username).exists():
            return render(request, "user/register.html", {"error": "Username already exists"})

    
        user = User.objects.create_user(username=username, password=password)

     
        profile = TouristProfile.objects.create(
            user=user,
            aadhaar_number=aadhaar,
            pan_number=pan,
            days_of_stay=days,
            
            verified=verified
        )

       
        UserLocation.objects.create(user=user, latitude=0.0, longitude=0.0)

     
        login(request, user)

        tourist_id = str(uuid.uuid4())
        valid_from = int(time.time())
        valid_to = valid_from + days * 24 * 3600

        if add_tourist is not None:
            try:
                tx = add_tourist(tourist_id, username, aadhaar, valid_from, valid_to)
                print("Blockchain tx:", tx)
            except Exception as e:
                print("Blockchain add_tourist failed:", e)

        if qrcode is not None:
            media_dir = getattr(settings, "MEDIA_ROOT", None)
            if media_dir:
                qr_dir = os.path.join(media_dir, "qrcodes")
                os.makedirs(qr_dir, exist_ok=True)

                verify_url = f"http://127.0.0.1:8000/blockchain/verify/{tourist_id}/"
                qr_path = os.path.join(qr_dir, f"{tourist_id}.png")

                try:
                    img = qrcode.make(verify_url)   
                    img.save(qr_path)
                    profile.qr_code = f"qrcodes/{tourist_id}.png"
                    profile.save()
                except Exception as e:
                    print("QR creation failed:", e)


        return redirect("user:dashboard")

    return render(request, "user/register.html")


@login_required
def dashboard(request):
    profile = TouristProfile.objects.get(user=request.user)
    return render(request, "user/dashboard.html", {"profile": profile})

from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("user:dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "user/login.html", {"form": form})

def home(request):
    return render(request, "user/home.html")
