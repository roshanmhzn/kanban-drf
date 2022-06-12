from rest_framework import serializers

from .models import Board


class BoardListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Board
        fields = ('id', 'user', 'name','created_at')

class BoardDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Board
        fields = ( 'user', 'name','created_at')
