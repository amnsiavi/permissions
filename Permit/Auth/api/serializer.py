from rest_framework import serializers
from django.contrib.auth.models import User


class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username','email','password','is_superuser']


