from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.models import TouristProfile
from track.models import UserLocationHistory
from user.serializers import TouristProfileSerializer
from track.serializers import UserLocationHistorySerializer

@api_view(["POST"])
def register_mobile(request):
    serializer = TouristProfileSerializer(data=request.data)
    if serializer.is_valid():
        profile = serializer.save()
        return Response({"success": True, "message": "Registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_mobile(request):
    username = request.data.get("username")
    try:
        user = TouristProfile.objects.get(username=username)
        if hasattr(user, "touristprofile") and user.touristprofile.verified:
            return Response({"success": True, "message": "Login success"})
        else:
            return Response({"success": False, "message": "User not verified"}, status=status.HTTP_403_FORBIDDEN)
    except TouristProfile.DoesNotExist:
        return Response({"success": False, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def qr_mobile(request, user_id):
    try:
        user = TouristProfile.objects.get(id=user_id)
        
        qr_code_url = f"/media/qrcodes/{user.username}.png"  
        return Response({"success": True, "qr": qr_code_url})
    except TouristProfile.DoesNotExist:
        return Response({"success": False, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def location_mobile(request):
    serializer = UserLocationHistorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "Location saved"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
