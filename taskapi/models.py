from boardapi.models import Board
from django.db import models

from columnapi.models import Column


class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    status = models.BooleanField()
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    index = models.IntegerField() # represents the position of task in a column

    def __str__(self):
        return self.title
    
