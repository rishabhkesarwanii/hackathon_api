#Import from django Library
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login
from django.utils import timezone

#Import from rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import permissions

#Import from models, forms, serializers
from .models import Hackathon, RegisterHackathon, UserProfile
from .forms import HackathonForm, SubmissionForm
from .serializers import HackathonSerializer, UserSerializer, RegisterSerializer, HackathonSubmissionSerializer

#Import from knox
from knox.models import AuthToken
from knox.views import LoginView

#Import from extras
import validators


#Register a user
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data, #serialized representation of a user object
        "token": AuthToken.objects.create(user)[1]
        })

#Login a user
class LoginAPI(LoginView):
    permission_classes = (permissions.AllowAny,)  #Allow any user to login(send request)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data) #data=request.data is the data that is sent in the request
        serializer.is_valid(raise_exception=True) #raise_exception=True is to raise an exception if the serializer is not valid
        user = serializer.validated_data['user'] #validated_data is the data after it has been validated
        login(request, user) #login the user
        return super(LoginAPI, self).post(request, format=None)




#View to List all Hackathons
class HackathonListView(APIView):
    permission_classes = (permissions.IsAuthenticated,) #Only authenticated users can view this page
    def get(self, request):
        hackathons = Hackathon.objects.all() #Get all the hackathons
        serializer = HackathonSerializer(hackathons, many=True) #Serialize the hackathons
        return Response({"hackathons": serializer.data})
    


#View to List one Hackathons filter by id
class HackathonListOneView(APIView):
    permission_classes = (permissions.IsAuthenticated,) #Only authenticated users can view this page
    def get(self, request, pk):
        hackathon = get_object_or_404(Hackathon, id=pk) #Get the hackathon with the id=pk(primary key)
        serializer = HackathonSerializer(hackathon) #Serialize the hackathon
        return Response(serializer.data)


#View to Create a new Hackathon
class HackathonCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,) #Only authenticated users can view this page
    serializer_class = HackathonSerializer #Use the HackathonSerializer to serialize the data
    
    def post(self, request, *args, **kwargs):
        user = request.user
        form = HackathonForm(request.POST, request.FILES) #Get the data from the form with files
        if form.is_valid():
            hackathon_saved = form.save(commit=False) #Save the data but don't commit it to the database
            hackathon_saved.user_profile = user #Set the user_profile to the user that is logged in
            hackathon_saved.save() #Save the data to the database
            serializer = HackathonSerializer(hackathon_saved) #Serialize the data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)




#View to Update a Hackathon
class HackathonUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,) #Only authenticated users can view this page
    serializer_class = HackathonSerializer #Use the HackathonSerializer to serialize the data
    queryset = Hackathon.objects.all() #Get all the hackathons

    def put(self, request, *args, **kwargs):
        hackathon_id = kwargs.get('pk') #Get the id of the hackathon
        hackathon = get_object_or_404(Hackathon, id=hackathon_id) #Get the hackathon with the id

        user = request.user #Get the user that is logged in
        if hackathon.user_profile != user: #Check if the user that is logged in is the user that created the hackathon
            return Response({"error": "User is not authorized to edit this hackathon."}, status=status.HTTP_403_FORBIDDEN) #Return an error if the user is not the user that created the hackathon
        check = hackathon.type_of_submission #Get the type of submission of the hackathon
        form = HackathonForm(request.POST or None, request.FILES or None, instance=hackathon) #Get the data from the form with files
        if form.is_valid():
            hackathon_saved = form.save(commit=False)
            if timezone.now() > hackathon.start_datetime and check != hackathon_saved.type_of_submission: #Check if the hackathon has already started and the type of submission is changed
                return Response({"error": "Hackathon has already started. You cannot edit type  of submission."}, status=status.HTTP_403_FORBIDDEN) #Return an error if the hackathon has already started
            hackathon_saved.user_profile = user #Set the user_profile to the user that is logged in
            hackathon_saved.save() #Save the data to the database
            serializer = HackathonSerializer(hackathon_saved) #Serialize the data
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


#Register a user to a hackathon(A user can register only once to a hackathon)
class HackathonRegisterView(APIView):
    permission_classes = (permissions.IsAuthenticated,) #Only authenticated users can view this page
    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile = UserProfile.objects.get(user=user.id) #Get the user profile of the user
        hackathon_id = kwargs.get('pk') #Get the id of the hackathon
        hackathon = Hackathon.objects.get(id=hackathon_id) #Get the hackathon with the id
        
        registration = RegisterHackathon(user_profile=user_profile, hackathon=hackathon) #Create a new registration
        try:
            registration.save() #Save the registration
            return Response({"success": "User '{}' registered for hackathon '{}'".format(user.username, hackathon.title)}) #Return a success message
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) #Return an error message if the user is already registered to the hackathon



#View to List all Hackathons registered by a user
class HackathonRegisteredListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,) #Only authenticated users can view this page
    serializer_class = HackathonSerializer #Use the HackathonSerializer to serialize the data
    

    def get_queryset(self):
        user = self.request.user #Get the user that is logged in
        registered_hackathons = RegisterHackathon.objects.filter(user_profile=user.userprofile).values_list('hackathon') #Get all the hackathons that the user is registered to
        queryset = Hackathon.objects.filter(pk__in=registered_hackathons) #Get all the hackathons that the user is registered to
        return queryset
    


#View to List all Hackathons registered by a user
class HackathonSubmissionView(APIView):
    permission_classes = (permissions.IsAuthenticated,) #Only authenticated users can view this page
    serializer_class = HackathonSubmissionSerializer #Use the HackathonSubmissionSerializer to serialize the data

    def get(self, request, pk):
        user_profile = request.user.userprofile #Get the user profile of the user
        hackathon = get_object_or_404(Hackathon, pk=pk) #Get the hackathon with the id
        submissions = RegisterHackathon.objects.filter(user_profile=user_profile, hackathon=hackathon) #Get all the submissions of the user to the particular hackathon
        serializer = self.serializer_class(submissions, many=True) #Serialize the data
        return Response(serializer.data)
    
    def post(self, request, pk):
        user_profile = request.user.userprofile #Get the user profile of the user
        hackathon = get_object_or_404(Hackathon, pk=pk) #Get the hackathon with the id
        register_hackathon = get_object_or_404(RegisterHackathon, user_profile=user_profile, hackathon=hackathon) #Get the registration of the user to the hackathon
        form = SubmissionForm(request.POST or None, request.FILES or None, instance=register_hackathon) #Get the data from the form with files

        submission_type = hackathon.type_of_submission #Get the type of submission for the hackathon from the database

        
        if form.is_valid():
            check = form.save(commit=False) #Save the data but don't commit it to the database
            serializer = self.serializer_class(register_hackathon) #Serialize the data

            if register_hackathon.is_submitted: #Check if the user has already submitted
                return Response({"error": "Hackathon has already been submitted."}, status=status.HTTP_400_BAD_REQUEST) #Return an error if the user has already submitted
            else:

                try: #Check if the submission type is valid
                    if submission_type == 'image': 
                        check.submission_image.file.content_type.index('image') #Check if the file is an image
                    elif submission_type == 'file':
                        check.submission_file.file.content_type.index('application') #Check if the file is an application
                    elif submission_type == 'link':
                        validators.url(check.submission_link) #Check if the link is valid
                except:
                    return Response({"error": f"Invalid submission type. Please check the submission type: {submission_type}."}, status=status.HTTP_400_BAD_REQUEST) #Return an error if the submission type is invalid

                else:
                    register_hackathon.is_submitted = True #Set the is_submitted field to True
                    check.save() #Save the data to the database
                    return Response(serializer.data,status=status.HTTP_200_OK)

        return Response({"error": "Invalid submission or not submitted."}, status=status.HTTP_400_BAD_REQUEST) #Return an error if the submission is invalid or not submitted


class HackathonListSubmissionView(APIView):
        permission_classes = (permissions.IsAuthenticated,) 
        serializer_class = HackathonSubmissionSerializer
        def get(self, request):
            user_profile = request.user.userprofile #Get the user profile of the user
            submissions = RegisterHackathon.objects.filter(user_profile=user_profile) #Get all the submissions of the user 
            serializer = self.serializer_class(submissions, many=True) #Serialize the data
            return Response(serializer.data)
