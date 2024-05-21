from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    types = (
        ('1', 'EDW'),
        ('2', 'OHB'),
    )

    user_id = models.CharField('ID', max_length=15, unique=True)
    user_name=models.CharField('名前', max_length=15, unique=True)
    job = models.CharField("タイプ", max_length=15, choices=types, blank=True, default='1')
    user_no = models.IntegerField('No', default=0)
