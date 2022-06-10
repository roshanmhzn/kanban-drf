from rest_framework import serializers

from .models import Board
from django.contrib.auth import get_user_model


class BoardListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Board
        fields = ('id', 'user', 'name','created_at')

class BoardDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Board
        fields = ( 'user', 'name','created_at')
