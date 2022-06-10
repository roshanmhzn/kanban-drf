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
    
    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self, request, pk):
        task = self.get_object(pk)
        if not BoardColumn.objects.filter(board_id=request.data['board'], column_id=request.data['column']):
            context = {"message": "The BoardColumn Relation does not exist"}
            return Response(context, status=status.HTTP_403_FORBIDDEN)            
        serializer = TaskSerializer(task, data=request.data)

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
