from rest_framework import serializers

from .models import BoardColumn


class BoardColumnSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BoardColumn
        fields = ('id', 'board_id', 'column_id')
