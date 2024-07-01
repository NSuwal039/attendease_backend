from rest_framework import serializers
from ..models import Student, StudentSubjectConfig

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentSubjectConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubjectConfig
        fields = '__all__'