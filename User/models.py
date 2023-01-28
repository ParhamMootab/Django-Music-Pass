from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.IntegerField(auto_created = True, primary_key = True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return super().__str__()