from django.urls import path

from .views import BoardListCreate

urlpatterns = [
    path('', BoardListCreate.as_view(), name='board_list_create'),
]
