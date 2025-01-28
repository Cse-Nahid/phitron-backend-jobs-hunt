from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):   
    job_seeker = serializers.StringRelatedField(many=False)

    class Meta:
        model = Application
        fields = ['id', 'job', 'job_seeker', 'resume', 'cover_letter']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if not request:
            raise ValueError("Request context is missing")
        user = request.user
        validated_data['job_seeker'] = user
        return super().create(validated_data)


