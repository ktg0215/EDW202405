from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from django.utils import timezone
from django.conf import settings
from user.models import CustomUser

SUB_START = (
    
    ('1','6'),
    ('2','7'),
    ('3','8'),
    ('4','8.5'),
    ('5','9'),
    ('6','9.5'),
    ('7','10'),
    ('8','11'),
    ('9','12'),
    ('10','13'),
    ('11','13.5'),
    ('12','14'),
    ('13','14.5'),
    ('14','15'),
    ('15','15.5'),
    ('16','16'),
    ('17','16.5'),
    ('18','17'),
    ('19','17.5'),
    ('20','18'),
    ('21','18.5'),
    ('22','19'),

)
SUB_END = (
    
    ('1','8.5'),
    ('2','9'),
    ('3','11'),
    ('4','12'),
    ('5','13'),
    ('6','14'),
    ('7','14.5'),
    ('8','15'),
    ('9','15.5'),
    ('10','16'),
    ('11','16.5'),
    ('12','17'),
    ('13','18'),
    ('14','19'),
    ('15','20'),
    ('16','20.5'),
    ('17','21'),
    ('18','22'),



)

class Schedule(models.Model):
    """スケジュール"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー', on_delete=models.SET_NULL, blank=True, null=True,related_name = "user_schedule")
    start_time = models.CharField('開始時間', choices= SUB_START, max_length=50,blank=True,default=0)
    end_time = models.CharField('終了時間', choices= SUB_END, max_length=50,blank=True,default=0)
    date = models.DateField('日付')

    def __str__(self):
        return f"{self.user.user_name} {self.date}{self.start_time}"


