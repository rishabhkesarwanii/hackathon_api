from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #one to one relationship with the User model
    
    def __str__(self):
        return self.user.username


class Hackathon(models.Model):

    HACKATHON_TYPES = (
        ('image', 'Image'),
        ('file', 'File'),
        ('link', 'Link'),
    )
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE) #one to many relationship with the User model
    title = models.CharField(max_length=255) 
    description = models.TextField()
    background_image = models.ImageField(upload_to='hackathons/background_images/') #upload_to is the path where the image will be stored
    hackathon_image = models.ImageField(upload_to='hackathons/hackathon_images/') #upload_to is the path where the image will be stored
    type_of_submission = models.CharField(max_length=50, choices=HACKATHON_TYPES)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reward_prize = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.title



class RegisterHackathon(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE) #one to many relationship with the UserProfile model
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE) #one to many relationship with the Hackathon model
    
    submission_name = models.CharField(max_length=255, blank=True, null=True)
    submission_summary = models.TextField(null=True, blank=True)
    submission_image = models.ImageField(upload_to='hackathons/submissions/image', blank=True, null=True)
    submission_file = models.FileField(upload_to='hackathons/submissions/file', blank=True, null=True)
    submission_link = models.URLField(null=True, blank=True)
    is_submitted = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user_profile', 'hackathon']
    

    def __str__(self):
        return f'{self.user_profile} registered for {self.hackathon}'


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    
post_save.connect(post_user_created_signal, sender=User)