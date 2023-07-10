from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=4, null=True, blank=True)
    birth_date = models.DateField(null=True)


    USERNAME_FIELD = 'username'


    def __str__(self):
        return self.username


