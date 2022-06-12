from functools import partial

from django.template import context
from boardcolumnapi.models import BoardColumn
from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer
from boardapi.models import Board
from columnapi.models import Column



class TaskListCreate(APIView):
    """
    View to list all Tasks and create a new Task in the system.
    """

    def get(self, request):
        """
        Return a list of all Tasks
        """
        Tasks = Task.objects.all().order_by('board','column', 'index')
        serializer = TaskSerializer(Tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create a new Task in the system
        """
        if not BoardColumn.objects.filter(board_id=request.data['board'], column_id=request.data['column']):
            context = {"message": "The BoardColumn Relation does not exist"}
            return Response(context, status=status.HTTP_403_FORBIDDEN)

        serializer = TaskSerializer(data=request.data)        
        if not serializer.is_valid():
           return Response(status=status.HTTP_403_FORBIDDEN)
        
        board = Board.objects.filter(id=request.data['board'])
        column = Column.objects.filter(pk=request.data['column'])

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
            boardid = serializer.validated_data['board']
            columnid = serializer.validated_data['column']
            task_index = serializer.validated_data['index']
            if Task.objects.filter(board=boardid, column=columnid, index=task_index).exists():
                content = {'message': 'The Task with this Index already exists'}
                return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)    
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetail(APIView):
    """
    Retrieve, update or delete a Task instance.
    """

    def get_object(self,pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404
    
    def check_board_column(self, pk, request_data):
        #check the datatype of board
        if type(request_data['board']) is not int or type(request_data['column']) is not int:
            msg = "INVALID BOARD AND COLUMN DATATYPE"
            if type(request_data['board']) is int and type(request_data['column']) is not int:
                msg = "INVALID COLUMN DATATYPE"
            if type(request_data['board']) is not int and type(request_data['column']) is int:
                msg = "INVALID BOARD DATATYPE"
            context = {"message": msg}
            return '0', context
         #check if the board column relation exists
        if not BoardColumn.objects.filter(board_id=request_data['board'], column_id=request_data['column']):
            context = {"message": "The BoardColumn Relation does not exist"}
            return '0', context
        return '1'
        
        

    def check_serializer_validity(self, serializer):
        
        if not serializer.is_valid():
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        if serializer.is_valid():
            if 'board' in serializer.validated_data:
                board = serializer.validated_data['board']
                column = serializer.validated_data['column']
                task_objects = Task.objects.filter(board_id=board.id, column_id=column.id) # get all the tasks from the Task
                if not task_objects:
                    serializer.validated_data['index'] = 1
                else:
                    task_indexes = []
                    new_index = None
                    for task_object in task_objects:
                        task_indexes.append(task_object.index)
                    max_index = max(task_indexes)
                    for i in range(1, max_index+1):
                        if i not in task_indexes:
                            new_index = i
                            break
                    if new_index is None:
                        new_index = max_index + 1
                    serializer.validated_data['index'] = new_index   
                serializer.save()
                return serializer
            serializer.save()
            return serializer
    
    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self, request, pk):
        task = self.get_object(pk)
        print(self.check_board_column(pk, request.data))
        board_column = self.check_board_column(pk, request.data)  
        # import pdb;pdb.set_trace()
        if '0' in board_column: 
            return Response(board_column[1], status=status.HTTP_403_FORBIDDEN)     
        serializer = TaskSerializer(task, data=request.data)

        serialized_data = self.check_serializer_validity(serializer)
        
        # Extra level if above doesn't work
        # board = Board.objects.filter(id=request.data['board'])
        # column = Column.objects.filter(pk=request.data['column'])
        # if not (board and column):
        #     msg = 'INVALID BOARD AND COLUMN'
        #     if board and not column:
        #         msg = 'INVALID COLUMN'
        #     elif not board and column:
        #         msg = 'INVALID BOARD'                
        #     print(board, column)
        #     content = {'message': msg}
        #     return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        return Response(serialized_data.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        task = self.get_object(pk)
        if 'board' in request.data and 'column' in request.data:
            board_column = self.check_board_column(pk, request.data)  
            if '0' in board_column: 
                return Response(board_column[1], status=status.HTTP_403_FORBIDDEN)  
        if ('board' in request.data and 'column' not in request.data
        ) or ('board' not in request.data and 'column' in request.data
        ) or ('board' not in request.data and 'column' not in request.data and 'index' in request.data):
            context = {"message": "The Board, Column & Index Must Pass if Index is present AND Board & \
             Column cannot be passed solo"}
            return Response(context, status=status.HTTP_403_FORBIDDEN)
        serializer = TaskSerializer(task, data=request.data, partial=True)           
        serialized_data = self.check_serializer_validity(serializer)
        return Response(serialized_data.data, status=status.HTTP_201_CREATED)


    # def patch(self, request, pk):
    #     task = self.get_object(pk)
    #     serializer = TaskSerializer(task, data=request.data, partial=True) # set partial=True to update a data partially
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        Task = self.get_object(pk)
        Task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskBoard(APIView):
    def get_board_objects(self, bid):
        results = Task.objects.filter(board_id=bid).order_by('board_id')
        if results:
            return results
        raise Http404  

    def get_board_column_objects(self, bid, cid):
        results = Task.objects.filter(board_id=bid, column_id=cid).order_by('board_id', 'column_id')
        if results:
            return results
        raise Http404  

    def get(self, request, *args, **kwargs):
        if 'column_id' in kwargs:
            tasks = self.get_board_column_objects(kwargs['board_id'], kwargs['column_id'])
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)

        tasks = self.get_board_objects(kwargs['board_id'])
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskBoardStatus(APIView):

    def get_board_column_objects(self, bid, cid, status):  
        results = Task.objects.filter(board_id=bid, column_id=cid,status=status).order_by('board_id', 'column_id')
        if results:
            return results
        raise Http404  

    def get(self, request, *args, **kwargs):
        if kwargs['status'] not in (0,1):
            context = {'message': 'The status value should be either 0 for False or 1 for True'}
            return Response(context, status=status.HTTP_406_NOT_ACCEPTABLE)
        tasks = self.get_board_column_objects(kwargs['board_id'], kwargs['column_id'], kwargs['status'])
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
