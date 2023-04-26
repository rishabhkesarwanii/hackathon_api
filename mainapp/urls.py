from django.urls import path, include
from knox import views as knox_views
from .views import (
    RegisterAPI, 
    LoginAPI,
    HackathonListView, 
    HackathonCreateView, 
    HackathonUpdateView,
    HackathonListOneView,
    HackathonRegisteredListView,
    HackathonRegisterView, 
    HackathonSubmissionView,
    HackathonListSubmissionView,
    )

urlpatterns = [
    
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),

    
    path('hackathons/', HackathonListView.as_view()),
    path('hackathons/create/', HackathonCreateView.as_view()),
    path('hackathons/<int:pk>/', HackathonListOneView.as_view()),
    path('hackathons/<int:pk>/update/', HackathonUpdateView.as_view()),
    path('hackathons/registered/', HackathonRegisteredListView.as_view()),
    path('hackathons/<int:pk>/register/', HackathonRegisterView.as_view()),
    path('hackathons/<int:pk>/submit/', HackathonSubmissionView.as_view()),
    path('hackathons/listallsubmssions/', HackathonListSubmissionView.as_view()),


]