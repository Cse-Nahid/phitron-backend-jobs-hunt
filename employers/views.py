from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.generics import RetrieveUpdateAPIView
from .models import EmployerProfile
from .serializers import EmployerProfileSerializer, EmployerRegistrationSerializer
from applications.models import Application
from applications.serializers import ApplicationSerializer
from jobs.models import Job
from jobs.serializers import JobSerializer
from dj_rest_auth.views import LoginView as RestAuthLoginView, LogoutView as RestAuthLogoutView
from django.contrib.sessions.models import Session

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny

from .serializers import LoginSerializer, UserAccountSerializer

from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

# Profile Views

User = get_user_model()

class EmployerProfileListCreateView(APIView):
    def get(self, request):
        profiles = EmployerProfile.objects.all()
        serializer = EmployerProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployerProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployerProfileDetailView(APIView):

    def get_object(self):
        return EmployerProfile.objects.get(user=self.request.user)

    def get(self, request):
        profile = self.get_object()
        serializer = EmployerProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = self.get_object()
        serializer = EmployerProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        profile = self.get_object()
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployerProfileViewSet(viewsets.ModelViewSet):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer


class EmployerProfileUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployerProfileSerializer

    def get_object(self):
        return EmployerProfile.objects.get(user=self.request.user)

    def put(self, request):
        profile = self.get_object()
        serializer = EmployerProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Registration and Authentication
class EmployerRegistrationView(generics.CreateAPIView):
    serializer_class = EmployerRegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            email_subject = "Welcome to job hunt!"
            email_body = render_to_string("welcome_email.html", {"user": user})
            email = EmailMultiAlternatives(email_subject, "", to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            return Response(
                {"message": "Registration successful. Check your email for a welcome message."},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Dashboard and Applications Views
class EmployerDashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, 'employerprofile'):
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

        jobs = Job.objects.filter(employer=user)
        jobs_data = JobSerializer(jobs, many=True).data

        applications = Application.objects.filter(job__in=jobs)
        applications_data = ApplicationSerializer(applications, many=True).data

        return Response({
            'jobs': jobs_data,
            'applications': applications_data
        })


class EmployerApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employer_id = request.user.id
        jobs = Job.objects.filter(employer_id=employer_id)
        applications = Application.objects.filter(job__in=jobs)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)






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




class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"success": True, "message": "Logout successful."}, status=status.HTTP_200_OK)
