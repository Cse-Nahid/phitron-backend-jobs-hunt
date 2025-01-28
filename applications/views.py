from django.http import Http404
from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Application
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .serializers import ApplicationSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import logging
from rest_framework import generics, permissions


class ApplicationListCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ApplicationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            application = serializer.save(job_seeker=request.user)
            

            # Send email to the employer
            try:
                employer = application.job.employer
                email_subject = "New Job Application Received"
                email_body = render_to_string("new_application_email.html", {"employer": employer, "application": application})
                
                email = EmailMultiAlternatives(email_subject, "", to=[employer.email])
                email.attach_alternative(email_body, "text/html")
                email.send()
            except Exception as e:
                print(f"Error sending email to employer: {e}")

            # Send email  to the job seeker
            try:
                job_seeker = application.job_seeker
                email_subject = "Application Submitted Successfully"
                email_body = render_to_string("application_success_email.html", {"user": job_seeker, "job": application.job})
                email = EmailMultiAlternatives(email_subject, "", to=[job_seeker.email])
                email.attach_alternative(email_body, "text/html")
                email.send()
            except Exception as e:
                print(f"Error sending email to job seeker: {e}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ApplicationDetailView(APIView):
    def get_object(self, pk):
        try:
            return Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        application = self.get_object(pk)
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)

    def delete(self, request, pk):
        application = self.get_object(pk)
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ApplicationUpdateView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        application = self.get_object()

        if application.job_seeker != request.user:
            return Response({"error": "You are not authorized to edit this application."},
                            status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)
    
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    
    
class ApplicationDeleteView(generics.DestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        application = self.get_object()

        if application.job_seeker != request.user:
            return Response({"error": "You are not authorized to delete this application."},
                            status=status.HTTP_403_FORBIDDEN)

        application.delete()
        return Response({"message": "Application deleted successfully."}, status=status.HTTP_204_NO_CONTENT)