from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Job, JobCategory
from .serializers import JobSerializer, JobCategorySerializer



class JobCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            job = serializer.save(employer=request.user)
            return Response(JobSerializer(job).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobListCreateView(APIView):
    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobDetailView(APIView):
    def get(self, request, pk):
        try:
            job = Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = JobSerializer(job)
        return Response(serializer.data)

class JobCategoryDetailView(APIView):
    def get(self, request, pk):
        try:
            category = JobCategory.objects.get(pk=pk)
        except JobCategory.DoesNotExist:
            return Response({"error": "Job category not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = JobCategorySerializer(category)
        return Response(serializer.data)



from rest_framework import viewsets

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)

class JobCategoryViewSet(viewsets.ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    
    
class JobSearchView(APIView):

    def get(self, request):
        query = request.query_params.get('q', None)
        if query:
            jobs = Job.objects.filter(title__icontains=query)
            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "Please write your Query."})



         
