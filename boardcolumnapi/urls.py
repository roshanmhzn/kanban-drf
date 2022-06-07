from django.urls import path

from .views import BoardColumnRelationListCreate, BoardColumnRelationDetail, BoardColumnList

urlpatterns = [
    path('boardcolumnrelations/', BoardColumnRelationListCreate.as_view(), name='boardvolumnrelation_list_create'),
    path('boardcolumnrelation/<int:pk>', BoardColumnRelationDetail.as_view(), name='BoardColumnRelation_detail'),
    path('boardcolumnrelations/bybid/<int:board_id>', BoardColumnList.as_view(), name='BoardColumnRelation_lists')
]