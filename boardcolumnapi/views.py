from django.http import Http404
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BoardColumnRelation
from .serializers import BoardColumnRelationSerializer


class BoardColumnRelationListCreate(APIView):
    """
    View to list all BoardColumnRelations and create a new BoardColumnRelation in the system.
    """

    def get(self, request):
        """
        Return a list of all BoardColumnRelations
        """
        board_columns = BoardColumnRelation.objects.all()
        serializer = BoardColumnRelationSerializer(board_columns, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create a new BoardColumnRelation in the system
        """
        serializer = BoardColumnRelationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BoardColumnRelationDetail(APIView):
    """
    Retrieve, update or delete a BoardColumnRelation instance.
    """

    def get_object(self,pk):
        try:
            return BoardColumnRelation.objects.get(pk=pk)
        except BoardColumnRelation.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        board_column = self.get_object(pk)
        serializer = BoardColumnRelationSerializer(board_column)
        return Response(serializer.data)
    
    def put(self, request, pk):
        board_column = self.get_object(pk)
        serializer = BoardColumnRelationSerializer(board_column, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # def delete(self, request, pk):
    #     board_column = self.get_object(pk)
    #     board_column.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
