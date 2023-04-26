from rest_framework import serializers #import serializers from rest_framework

from django.contrib.auth.models import User #import the User model

from .models import Hackathon, RegisterHackathon #import the Hackathon and RegisterHackathon models


# User Serializer
class UserSerializer(serializers.ModelSerializer): #ModelSerializer for the User model
    class Meta:
        model = User 
        fields = ('id', 'username', 'email') #fields that will be returned in the response



# Register Serializer
class RegisterSerializer(serializers.ModelSerializer): #ModelSerializer for the User model
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}   #This is to make sure that the password is not returned in the response

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password']) #create a new user

        return user #return the user



# Hackathon Serializer -> show  hackathon details
class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = ('id', 'title', 'description', 'background_image', 'hackathon_image', 'type_of_submission',
                'start_datetime', 'end_datetime', 'reward_prize', 'last_updated') 
        read_only_fields = ('id',) #fields that will be returned in the response and cannot be edited

    def validate(self, data):
        if data['end_datetime'] <= data['start_datetime']: #check if the end datetime is after the start datetime
            raise serializers.ValidationError("End datetime must be after start datetime.")
        return data


class HackathonSubmissionSerializer(serializers.ModelSerializer): #ModelSerializer for the RegisterHackathon model
    class Meta:
        model = RegisterHackathon
        fields = ('id', 'submission_name', 'submission_summary', 'submission_image','submission_file', 'submission_link')
        read_only_fields = ('id',)