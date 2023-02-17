from django.db import models
from django.contrib.sessions.models import Session as DjangoSession
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    tin = models.CharField(max_length=10, blank=True, null=True)
    ref_id = models.IntegerField(blank=True, null=True)
    has_overdue = models.BooleanField()
    employee = None
    glob_id = models.CharField(max_length=24, blank=True, null=True)
    middle_name = models.CharField(max_length=128, blank=True, null=True)
    is_head = models.BooleanField()
    dt_set_overdue = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_user'


class Session(DjangoSession):
    class Meta:
        managed = False
        db_table = 'django_session'
