from pyexpat import model
from unicodedata import name
from django.contrib.auth import get_user_model
from django.db import models

# from ..columnapi.models import Column
from columnapi.models import Column


User = get_user_model()

class Board(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    columns = models.ManyToManyField(Column, blank=True)

    def __str__(self):
        return self.name
