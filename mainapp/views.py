from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import permissions

from .models import Hackathon, RegisterHackathon, UserProfile
from .forms import HackathonForm, SubmissionForm
from .serializers import HackathonSerializer, UserSerializer, RegisterSerializer, HackathonSubmissionSerializer


from knox.models import AuthToken
from knox.views import LoginView



class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(LoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)




#create a class based view to using django rest framework to show all hackathons
class HackathonView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        hackathons = Hackathon.objects.all()
        print(hackathons)
        serializer = HackathonSerializer(hackathons, many=True)
        return Response({"hackathons": serializer.data})
    


class HackathonOneView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, pk):
        hackathon = get_object_or_404(Hackathon, id=pk)
        serializer = HackathonSerializer(hackathon)
        return Response(serializer.data)



class HackathonCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = HackathonSerializer
    
    def post(self, request, *args, **kwargs):
        user = request.user
        form = HackathonForm(request.POST, request.FILES)
        if form.is_valid():
            hackathon_saved = form.save(commit=False)
            hackathon_saved.user_profile = user
            hackathon_saved.save()
            serializer = HackathonSerializer(hackathon_saved)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

from django.utils import timezone



class HackathonUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = HackathonSerializer
    queryset = Hackathon.objects.all()

    def put(self, request, *args, **kwargs):
        hackathon_id = kwargs.get('pk')
        hackathon = get_object_or_404(Hackathon, id=hackathon_id)
        if timezone.now() > hackathon.start_datetime:
            return Response({"error": "Hackathon has already started. You cannot edit this hackathon."}, status=status.HTTP_403_FORBIDDEN)
        user = request.user
        if hackathon.user_profile != user:
            return Response({"error": "User is not authorized to edit this hackathon."}, status=status.HTTP_403_FORBIDDEN)
        
        form = HackathonForm(request.POST or None, request.FILES or None, instance=hackathon)
        if form.is_valid():
            hackathon_saved = form.save(commit=False)
            hackathon_saved.user_profile = user
            hackathon_saved.save()
            serializer = HackathonSerializer(hackathon_saved)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


#Register a user to a hackathon
class RegisterHackathonView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile = UserProfile.objects.get(user=user.id)
        hackathon_id = kwargs.get('pk')
        hackathon = Hackathon.objects.get(id=hackathon_id)
        
        registration = RegisterHackathon(user_profile=user_profile, hackathon=hackathon)
        try:
            registration.save()
            return Response({"success": "User '{}' registered for hackathon '{}'".format(user.username, hackathon.title)})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class RegisteredHackathonListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = HackathonSerializer
    

    def get_queryset(self):
        user = self.request.user

        registered_hackathons = RegisterHackathon.objects.filter(user_profile=user.userprofile).values_list('hackathon')
        queryset = Hackathon.objects.filter(pk__in=registered_hackathons)
        return queryset
    


# class HackathonSubmissionView(APIView):
#     serializer_class = HackathonSubmissionSerializer

#     def get(self, request):
#         user_profile = request.user.userprofile
#         submissions = RegisterHackathon.objects.filter(user_profile=user_profile)
#         serializer = self.serializer_class(submissions, many=True)
#         return Response(serializer.data)

#     def post(self, request, pk):
#         user_profile = request.user.userprofile
#         submission_data = request.data

#         try:
#             hackathon = Hackathon.objects.get(id=pk)
#         except Hackathon.DoesNotExist:
#             return Response({'error': 'Hackathon does not exist'}, status=status.HTTP_404_NOT_FOUND)

#         if hackathon.type_of_submission == 'link':
#             submission_data.pop('submission_media', None)
#         else:
#             submission_data.pop('submission_link', None)

#         submission_data['user_profile'] = user_profile.id
#         submission_data['hackathon'] = hackathon.id

#         serializer = self.serializer_class(data=submission_data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class HackathonSubmissionView(APIView):
    serializer_class = HackathonSubmissionSerializer

    def get(self, request, pk):
        user_profile = request.user.userprofile
        hackathon = get_object_or_404(Hackathon, pk=pk)
        submissions = RegisterHackathon.objects.filter(user_profile=user_profile, hackathon=hackathon)
        serializer = self.serializer_class(submissions, many=True)
        return Response(serializer.data)
    
    # TODO 
    # - Add validation for submission type
    # - CANNOT EDIT AFTER SUBMISSION 
    def post(self, request, pk):
        user_profile = request.user.userprofile
        hackathon = get_object_or_404(Hackathon, pk=pk)
        register_hackathon = get_object_or_404(RegisterHackathon, user_profile=user_profile, hackathon=hackathon)
        form = SubmissionForm(request.POST or None, request.FILES or None, instance=register_hackathon)

        if form.is_valid():
            form.save()
            serializer = self.serializer_class(register_hackathon)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
