from django.contrib import admin

#Register your models here.

from .models import Zone


admin.site.register(Zone)  #to make it visible on admin page