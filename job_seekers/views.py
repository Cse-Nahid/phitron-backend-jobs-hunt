from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from .models import JobSeekerProfile
from .serializers import JobSeekerProfileSerializer, JobSeekerRegistrationSerializer
from django.http import Http404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from applications.models import Application
from applications.serializers import ApplicationSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny

from .serializers import LoginSerializer, UserAccountSerializer

from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

class JobSeekerProfileListCreateView(APIView):
    def get(self, request):
        profiles = JobSeekerProfile.objects.all()
        serializer = JobSeekerProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobSeekerProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobSeekerProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return JobSeekerProfile.objects.get(user=self.request.user)
        except JobSeekerProfile.DoesNotExist:
            raise Http404

    def get(self, request):
        profile = self.get_object()
        serializer = JobSeekerProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = self.get_object()
        serializer = JobSeekerProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobSeekerProfileViewSet(viewsets.ModelViewSet):
    queryset = JobSeekerProfile.objects.all()
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated]

    


class JobSeekerProfileUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobSeekerProfileSerializer

    def get_object(self):
            return JobSeekerProfile.objects.get(user=self.request.user)

    def put(self, request):
        profile = self.get_object()
        serializer = JobSeekerProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Registration
class JobSeekerRegistrationView(generics.CreateAPIView):
    serializer_class = JobSeekerRegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            email_subject = "Welcome to Job Hunt!"
            email_body = render_to_string("welcome_email.html", {"user": user})
            email = EmailMultiAlternatives(email_subject, "", to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            return Response(
                {"message": "Registration successful. Check your email for a welcome message."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Dashboard and Applications Views
class JobSeekerDashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, 'jobseekerprofile'):
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        applications = Application.objects.filter(job_seeker=user)
        applications_data = ApplicationSerializer(applications, many=True).data

        return Response({
            'applications': applications_data
        })


class JobSeekerApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        job_seeker = request.user
        applications = Application.objects.filter(job_seeker=job_seeker)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)



User = get_user_model()




# to get the user object data by an user_id
class UserDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        
        serializer = UserAccountSerializer(user)
        print('user:', serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)
class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Check if the account is active
            if user.is_active:
                # Generate or get the token for the user
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.id
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "This account is disabled."}, status=status.HTTP_403_FORBIDDEN)
        else:
            # Return error message for invalid credentials
            return Response({"detail": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)


# creating views for logout functionality
# class LogoutAPIView(APIView):
#     def get(self, request):
#         logout(request)
#         # return redirect('user_login')
#         return Response('Logout successful.')


class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"success": True, "message": "Logout successful."}, status=status.HTTP_200_OK)