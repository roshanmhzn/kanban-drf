from columnapi.models import Column
from boardapi.models import Board
from django.db import models


class BoardColumn(models.Model):
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)
    column_id = models.ForeignKey(Column, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.board_id.id) + '---' + \
        str(self.column_id.id) + '  ' + \
        str(self.board_id) + '---' + str(self.column_id)
