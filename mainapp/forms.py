from django import forms
from .models import Hackathon, RegisterHackathon

class HackathonForm(forms.ModelForm):
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
        # widgets = {
        #     'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        #     'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        # }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = RegisterHackathon
        fields = (
            'submission_name', 
            'submission_summary', 
            'submission_media', 
            'submission_link'
        )
        
        required = (
            'submission_name',
            'submission_summary',
        )