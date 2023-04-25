from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Hackathon, RegisterHackathon


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

class HackathonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Hackathon model.
    """
    class Meta:
        model = Hackathon
        fields = ('id', 'title', 'description', 'background_image', 'hackathon_image',
                'start_datetime', 'end_datetime', 'reward_prize', 'last_updated')
        read_only_fields = ('id',)

    def validate(self, data):
        """
        Custom validation for the Hackathon model.
        """
        if data['end_datetime'] <= data['start_datetime']:
            raise serializers.ValidationError("End datetime must be after start datetime.")
        return data


class HackathonSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterHackathon
        fields = ('id', 'submission_name', 'submission_summary', 'submission_media', 'submission_link')
        read_only_fields = ('id',)