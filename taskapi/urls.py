from django.urls import path

from .views import TaskListCreate, TaskDetail, TaskBoard

urlpatterns = [
    path('tasks/', TaskListCreate.as_view(), name='task_list_create'),
    path('task/<int:pk>', TaskDetail.as_view(), name='task_detail'),
    path('tasks/byid/<int:board_id>', TaskBoard.as_view(), name='task_board_lists'),
    path('tasks/bybidandcid/<int:board_id>/<int:column_id>', TaskBoard.as_view(), name='task_board_column_lists'),
]
