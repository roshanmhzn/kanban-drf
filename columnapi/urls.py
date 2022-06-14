from django.urls import path

from .views import ColumnListCreate, ColumnDetail, ColumnStatus

urlpatterns = [
    path('columns/', ColumnListCreate.as_view(), name='column_list_create'),
    path('columns/<int:status>', ColumnStatus.as_view(), name='column_list_status'),
    path('column/<int:pk>', ColumnDetail.as_view(), name='column_detail')
]
