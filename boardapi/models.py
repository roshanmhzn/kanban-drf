from django.contrib.auth import get_user_model
from django.db import models

from columnapi.models import Column


User = get_user_model()

class Board(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
