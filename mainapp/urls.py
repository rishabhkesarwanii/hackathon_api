from django.urls import path, include
from knox import views as knox_views
from .views import (
    HackathonView, 
    HackathonCreateView, 
    HackathonUpdateView,
    HackathonOneView,
    RegisteredHackathonListView,
    RegisterHackathonView, 
    HackathonSubmissionView,
    RegisterAPI, 
    LoginAPI)

urlpatterns = [
    
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),
    path('logoutall/', knox_views.LogoutAllView.as_view()),

    
    path('hackathons/', HackathonView.as_view()),
    path('hackathons/create/', HackathonCreateView.as_view()),
    path('hackathons/<int:pk>/', HackathonOneView.as_view()),
    path('hackathons/<int:pk>/update/', HackathonUpdateView.as_view()),
    path('hackathons/<int:pk>/register/', RegisterHackathonView.as_view()),
    path('hackathons/<int:pk>/submit/', HackathonSubmissionView.as_view()),
    path('hackathons/registered/', RegisteredHackathonListView.as_view()),

]