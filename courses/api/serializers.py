from rest_framework import serializers
from ..models import *

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class TeacherSubjectConfigSerializer(serializers.ModelSerializer):
    course_info = serializers.SerializerMethodField()
    subject_info = serializers.SerializerMethodField()
    
    def get_course_info(self, obj):
        return CourseSerializer(obj.course).data
    
    def get_subject_info(self, obj):
        return SubjectSerializer(obj.subject).data
    
    class Meta:
        model = TeacherSubjectConfig
        fields = '__all__'

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    period_info = serializers.SerializerMethodField()
    subject_info = serializers.SerializerMethodField()
    
    def get_period_info(self, obj):
        return PeriodSerializer(obj.period).data

    def get_subject_info(self, obj):
        return TeacherSubjectConfigSerializer(obj.subject).data
    
    class Meta:
        model = Class
        fields = '__all__'

# class AssignmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Assignment
#         fields = '__all__'

# class SubmittedAssignmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SubmittedAssignment
#         fields = '__all__'