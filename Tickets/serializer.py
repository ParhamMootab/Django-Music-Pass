from rest_framework import serializers
from . import models
from django.forms import ValidationError

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = ("seat_number", "user_id")
    
    def validate_seat_number(self, value):
        if value > 100 or value < 1 :
            raise ValidationError("Seat number must be between 1 and 100.")
        return value