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

class SubjectCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectCourse
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
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