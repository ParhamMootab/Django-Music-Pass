from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    user_id = models.IntegerField(auto_created = True, primary_key = True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self) -> str:
        return super().__str__()