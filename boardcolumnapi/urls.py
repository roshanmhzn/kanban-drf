from django.urls import path

from .views import BoardColumnListCreate, BoardColumnDetail, BoardColumnList

urlpatterns = [
    path('boardcolumns/', BoardColumnListCreate.as_view(), name='boardcolumn_list_create'),
    path('boardcolumn/<int:pk>', BoardColumnDetail.as_view(), name='boardcolumn_detail'),
    path('boardcolumns/<int:board_id>', BoardColumnList.as_view(), name='boardcolumn_lists')
]