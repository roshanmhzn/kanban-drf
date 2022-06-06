from django.urls import path

from .views import BoardListCreate, BoardDetail

urlpatterns = [
    path('boards/', BoardListCreate.as_view(), name='board_list_create'),
    path('board/<int:pk>', BoardDetail.as_view(), name='board_detail'),
]
