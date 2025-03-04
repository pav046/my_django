from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(blank=True, null=True, default=None, verbose_name='Фото', upload_to='users/%Y/%m/%d/')
    birth_date = models.DateField(blank=True, null=True, default=None, verbose_name='Дата рождения')