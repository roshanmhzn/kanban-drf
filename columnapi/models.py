from django.db import models

from boardapi.models import Board

class Column(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    index = models.IntegerField() # represents the position of column in a board
    status = models.BooleanField() # show/hide model
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name