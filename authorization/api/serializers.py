from rest_framework import serializers

from student.api.serializers import StudentSerializer
from teacher.api.serializers import TeacherSerializer
from ..models import CustomUser
from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    groups = serializers.SerializerMethodField()
    profile= serializers.SerializerMethodField()
    
    def get_groups(self, obj):
        return GroupSerializer(obj.groups, many=True).data
    
    def get_profile(self, obj):
        profile = None
        try:
            profile = obj.student
            return StudentSerializer(profile).data
        except:
            pass
        
        try:
            profile = obj.teacher
            return TeacherSerializer(profile).data
        except:
            pass

            

    class Meta:
        model = CustomUser
        fields = ['id','username', 'password', 'email', 'first_name', 'last_name', 'groups', 'profile']
    
    def create(self, validated_data):
        print('in serializer')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     password = validated_data.get('password', None)
    #     if password:
    #         instance.set_password(password)
    #     instance.save()
    #     return instance