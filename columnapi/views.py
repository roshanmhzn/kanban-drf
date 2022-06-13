from functools import partial
from django.http import Http404
from django.template import context

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Column
from .serializers import ColumnSerializer


class ColumnListCreate(APIView):
    """
    View to list all Columns and create a new Column in the system.
    """

    def get(self, request):
        """
        Return a list of all Columns
        """
        columns = Column.objects.all().order_by('index')
        serializer = ColumnSerializer(columns, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create a new Column in the system
        """
        serializer = ColumnSerializer(data=request.data)
        if serializer.is_valid():
            column_index = serializer.validated_data['index']
            if Column.objects.filter(index=column_index):
                content = {'message': 'The Column with this Index already exists'}
                return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class ColumnDetail(APIView):
    """
    Retrieve, update or delete a Column instance.
    """

    def get_object(self,pk):
        try:
            return Column.objects.get(pk=pk)
        except Column.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        column = self.get_object(pk)
        serializer = ColumnSerializer(column)
        return Response(serializer.data)
    
    def check_serializer_validity(self, serializer, pk, request):
        if not serializer.is_valid():
            return ('invalid',)
        if serializer.is_valid():
            if 'index' in serializer.validated_data:
                column_index = serializer.validated_data['index']
                current_column = Column.objects.get(pk=pk)
                current_column_task = current_column.index
                if current_column_task == column_index:
                    serializer.save()
                    return (serializer, 'valid')
                # import pdb; pdb.set_trace() 
                # print(current_column)
                if Column.objects.filter(index=column_index):
                    index_exist_content = {'message': 'The Column with this Index already exists'}
                    return (index_exist_content,status.HTTP_406_NOT_ACCEPTABLE)
            serializer.save()
            return (serializer, 'valid')
    
    def put(self, request, pk):
        column = self.get_object(pk)
        serializer = ColumnSerializer(column, data=request.data)
        check_validity = self.check_serializer_validity(serializer, pk, request)
        # import pdb;pdb.set_trace()
        if 'valid' in check_validity:
            # print(check_validity[0])
            return Response(check_validity[0].data)
        elif 'invalid' in check_validity:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            context = check_validity[0]
            # print(context)
            status_code = check_validity[1]
            return Response(context, status_code)

    def patch(self, request, pk):
        column = self.get_object(pk)
        serializer = ColumnSerializer(column, data=request.data, partial=True)
        check_validity = self.check_serializer_validity(serializer, pk, request)
        # import pdb;pdb.set_trace()
        if 'valid' in check_validity:
            # print(check_validity[0])
            return Response(check_validity[0].data)
        elif 'invalid' in check_validity:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            context = check_validity[0]
            # print(context)
            status_code = check_validity[1]
            return Response(context, status_code)
    
    def delete(self, request, pk):
        Column = self.get_object(pk)
        Column.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)