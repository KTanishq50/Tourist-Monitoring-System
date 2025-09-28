# USER MADE FILE


from django.shortcuts import render, redirect

def landing_page(request):
    return render(request, "proj1/landing.html")

def authority_home(request):
    return render(request, "proj1/authority_home.html")
