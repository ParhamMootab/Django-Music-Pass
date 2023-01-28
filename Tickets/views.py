from django.shortcuts import render
from rest_framework import views
from . import models, serializer
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class TicketingAPI(views.APIView):
    def get(self, request):
        db_objects = models.Ticket.objects.all()
        json_seialized = serializer.TicketSerializer(db_objects, many=True)
        return Response(json_seialized.data)
    
    def post(self, request):
        desirilized_data = serializer.TicketSerializer(data=request.data)
        if desirilized_data.is_valid():
            desirilized_data.save()
            return Response({
                "Type": "Success",
                "Message": "Your ticket for seat number {} is booked!".format(desirilized_data.validated_data.get("seat_number"))
            }, status=status.HTTP_200_OK)
        else:
            return Response(desirilized_data.errors, status=status.HTTP_400_BAD_REQUEST)

class SingleTicketAPI(views.APIView):
    def get(self, request, ticket_id):
        try:
            ticket = models.Ticket.objects.get(pk=ticket_id)
        except ObjectDoesNotExist:
            return Response({
                "Type": "Fail",
                "Message": "Ticket does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        json_seialized = serializer.TicketSerializer(ticket)
        return Response(json_seialized.data)
        