from columnapi.models import Column
from boardapi.models import Board
from django.db import IntegrityError, models


class BoardColumnRelation(models.Model):
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)
    column_id = models.ForeignKey(Column, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.board_id) + ' ' + str(self.column_id)

    # def save(self, *args, **kwargs):
    #     # print(self.board_id, self.column_id)
    #     if BoardColumnRelation.objects.filter(board_id=self.board_id, column_id=self.column_id).exists():
    #         raise IntegrityError
    #     else:
    #         super(BoardColumnRelation, self).save(*args, **kwargs)


    