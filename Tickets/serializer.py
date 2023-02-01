from rest_framework import serializers
from . import models
from django.forms import ValidationError

class TicketSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('context', {}).get('request')
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = models.Ticket
        fields = ["seat_number"]
    
    def create(self, validated_data):
        validated_data['user_id'] = self.request.user
        return super().create(validated_data)
    
    def validate_seat_number(self, value):
        if value > 100 or value < 1 :
            raise ValidationError("Seat number must be between 1 and 100.")
        return value