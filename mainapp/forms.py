from django import forms
from .models import Hackathon, RegisterHackathon

class HackathonForm(forms.ModelForm): #ModelForm for the Hackathon model
    class Meta:
        model = Hackathon
        fields = (
            'title', 
            'description', 
            'background_image', 
            'hackathon_image', 
            'type_of_submission', 
            'start_datetime', 
            'end_datetime', 
            'reward_prize'
        )

class SubmissionForm(forms.ModelForm): #ModelForm for the RegisterHackathon model
    class Meta:
        model = RegisterHackathon
        fields = (
            'submission_name', 
            'submission_summary', 
            'submission_image',
            'submission_file', 
            'submission_link'
        )
        
        required = (    #user has to fill in the required fields
            'submission_name',
            'submission_summary',
        )