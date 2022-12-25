from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework import serializers
from .models import User,Problem,ProblemTag,Record,Record_Tasks

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'is_superuser',
            'last_login',
            'username',
            'is_active',
            'is_staff',
            'date_joined',
        ]
class ProblemTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemTag
        fields = "__all__"
class Record_TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record_Tasks
        fields = "__all__"
class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = "__all__"