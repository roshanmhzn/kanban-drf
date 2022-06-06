from django.urls import path

from .views import BoardColumnRelationListCreate, BoardColumnRelationDetail

urlpatterns = [
    path('boardcolumnrelation/', BoardColumnRelationListCreate.as_view(), name='boardvolumnrelation_list_create'),
    path('boardcolumnrelation/<int:pk>', BoardColumnRelationDetail.as_view(), name='BoardColumnRelation_detail')
]