from rest_framework import serializers
from django.db import transaction
from .models import User, Project, Task
import re

PASSWORD_PATTERN = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"


class CreateNewPrimaryUserSerializer(serializers.ModelSerializer):
    

    def validate_password(self, value):
        if re.match(PASSWORD_PATTERN, value):
            return value
        else:
            raise serializers.ValidationError("Raised when password is smaller than 8 character and not using one upper, one lower and one special character.")


    def create(self, validated_data):
        with transaction.atomic():
            password = validated_data.pop('password')
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }


# Serializer for displaying user details
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'members', 'is_deleted', 'created_at']
        read_only_fields = ['owner', 'is_deleted', 'created_at']

    def create(self, validated_data):
        members = validated_data.pop('members', [])
        project = Project.objects.create(**validated_data)
        project.members.set(members)
        return project


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date', 'project', 'is_deleted', 'created_at','owner']
        read_only_fields = ['is_deleted', 'created_at']

    def create(self, validated_data):
        return Task.objects.create(**validated_data)
