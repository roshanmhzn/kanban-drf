from django.urls import path

from .views import ColumnListCreate, ColumnDetail

urlpatterns = [
    path('columns/', ColumnListCreate.as_view(), name='Column_list_create'),
    path('column/<int:pk>', ColumnDetail.as_view(), name='Column_detail')
]
