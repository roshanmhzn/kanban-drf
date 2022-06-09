from bdb import set_trace
from columnapi.models import Column
from msilib.schema import Class
from boardapi.models import Board
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
        # try:
        #     board = Board.objects.get(pk=request.data['board_id'])
        #     column = Column.objects.get(pk=request.data['column_id'])
        # except Board.DoesNotExist:
        #     content = {'message': 'INVALID BOARD ID'}
        #     return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)   
        # except Column.DoesNotExist:
        #     content = {'message': 'INVALID COLUMN ID'}
        #     return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = BoardColumnRelationSerializer(data=request.data)

        if not serializer.is_valid():
            board = Board.objects.filter(id=request.data['board_id'])
            column = Column.objects.filter(pk=request.data['column_id'])

            if not (board and column):
                msg = 'INVALID BOARD AND COLUMN'
                if board and not column:
                    msg = 'INVALID COLUMN'
                elif not board and column:
                    msg = 'INVALID BOARD'                
                print(board, column)
                content = {'message': msg}
                return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
                
    
        if serializer.is_valid():
            boardid = serializer.validated_data["board_id"]
            columnid = serializer.validated_data["column_id"]
           
            if BoardColumnRelation.objects.filter(board_id=boardid, column_id=columnid).exists():
                content = {'message': 'This Board and Column relation already exists'}
                return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)    
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


class BoardColumnList(APIView):

    def get_objects(self, board_id):
        results = BoardColumnRelation.objects.filter(board_id=board_id).order_by('board_id').order_by('board_id')
        if results:
            return results
        raise Http404    


    def get(self, request, board_id):
        board_columns = self.get_objects(board_id)
        serializer = BoardColumnRelationSerializer(board_columns, many=True)
        return Response(serializer.data)