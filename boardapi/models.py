from pyexpat import model
from unicodedata import name
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class Board(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
