from django.db import models

# Create your models here.
class Ticket(models.Model):
    id = models.IntegerField(primary_key = True, auto_created = True)
    seat_number = models.IntegerField()
    user_id = models.ForeignKey('User.User', on_delete=models.CASCADE)
    
    
    def __str__(self) -> str:
        return super().__str__()
    