from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Board
from .serializers import BoardSerializer


class BoardListCreate(APIView):
    """
    View to list all boards and create a new board in the system.
    """

    def get(self, request):
        """
        Return a list of all boards
        """
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create a new board in the system
        """
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
