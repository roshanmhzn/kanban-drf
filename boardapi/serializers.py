from rest_framework import serializers

from .models import Board
from django.contrib.auth import get_user_model


class BoardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Board
        fields = ('id', 'user', 'name')