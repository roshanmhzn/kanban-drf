from django.urls import path

from .views import TaskBoardStatus, TaskListCreate, TaskDetail, TaskBoard

urlpatterns = [
    path('tasks/', TaskListCreate.as_view(), name='task_list_create'),
    path('task/<int:pk>', TaskDetail.as_view(), name='task_detail'),
    path('tasks/<int:board_id>', TaskBoard.as_view(), name='task_board_lists'),
    path('tasks/<int:board_id>/<int:column_id>', TaskBoard.as_view(), name='task_board_column_lists'),
    # path('tasks/bybid/<int:board_id>/<int:status>', TaskBoardStatus.as_view(), name='task_board_status_lists'),
    path('tasks/<int:board_id>/<int:column_id>/<int:status>', TaskBoardStatus.as_view(), name='task_board_column_status_lists'),
]
