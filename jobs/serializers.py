from rest_framework import serializers
from .models import Job, JobCategory

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["id",'title', 'description', 'category',
                  'location', 'experience', 'employee_type', 'position', 'offer_salary'
                  , 'responsibilities', 'qualifications', 'skills_experience',"date_posted"]
        


class JobCategorySerializer(serializers.ModelSerializer):
    job_count = serializers.SerializerMethodField()
    jobs = JobSerializer(many=True, read_only=True)
    
    class Meta:
        model = JobCategory
        fields =  ['id', 'name', 'job_count', 'jobs']
    
    def get_job_count(self, obj):
        return Job.objects.filter(category=obj).count()
