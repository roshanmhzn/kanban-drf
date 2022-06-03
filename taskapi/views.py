from django.http import Http404
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer



class TaskListCreate(APIView):
    """
    View to list all Tasks and create a new Task in the system.
    """

    def get(self, request):
        """
        Return a list of all Tasks
        """
        Tasks = Task.objects.all().order_by('index')
        serializer = TaskSerializer(Tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create a new Task in the system
        """
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
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
        Task = self.get_object(pk)
        serializer = TaskSerializer(Task)
        return Response(serializer.data)
    
    def put(self, request, pk):
        Task = self.get_object(pk)
        serializer = TaskSerializer(Task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        Task = self.get_object(pk)
        Task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

