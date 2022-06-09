from django.http import Http404
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

class BoardDetail(APIView):
    """
    Retrieve, update or delete a board instance.
    """

    def get_object(self,pk):
        try:
            return Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise Http404
            # return Response({'message': 'The Board with id doesnot exist'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        # return Board.objects.filter(pk=pk)
            
    
    def get(self, request, pk):
        board = self.get_object(pk)
        # if not board:
        #     content = {'message': 'The Board with id doesnot exist'}
        #     return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = BoardSerializer(board)
        return Response(serializer.data)
    
    def put(self, request, pk):
        board = self.get_object(pk)
        serializer = BoardSerializer(board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        board = self.get_object(pk)
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
