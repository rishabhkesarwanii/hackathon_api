from django.contrib import admin
from .models import Hackathon, UserProfile, RegisterHackathon

# Register your models here.

admin.site.register(Hackathon) 
admin.site.register(UserProfile)
admin.site.register(RegisterHackathon)