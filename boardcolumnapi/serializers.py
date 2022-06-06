from rest_framework import serializers

from .models import BoardColumnRelation
from django.contrib.auth import get_user_model


class BoardColumnRelationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BoardColumnRelation
        fields = ('id', 'board_id', 'column_id')
