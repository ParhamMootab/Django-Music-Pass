from django.shortcuts import render
from rest_framework import views
from . import models, serializer
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class TicketingAPI(views.APIView):
    def get(self, request):
        try:
            from_seat = int(request.query_params['from'])
            to_seat = int(request.query_params['to'])
        except:
            from_seat = None
            to_seat = None
        if not from_seat or not to_seat:
            db_objects = models.Ticket.objects.all()
        else:
            db_objects = models.Ticket.objects\
            .filter(seat_number__gte = from_seat)\
            .filter(seat_number__lte = to_seat)
            
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
    def get(self, request, seat_number):
        try:
            seat = models.Ticket.objects.get(seat_number=seat_number)
        except ObjectDoesNotExist:
            return Response({
                "Type": "Fail",
                "Message": "Ticket does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        json_seialized = serializer.TicketSerializer(seat)
        return Response(json_seialized.data)
    
    def delete(self, request, seat_number):
        try:
            models.Ticket.objects.get(seat_number=seat_number).delete()
        except ObjectDoesNotExist:
            return Response({
                "Type": "Fail",
                "Message": "Ticket does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        return Response({
                "Type": "Success",
                "Message": "Ticket for the seat number {} was canceled.".format(seat_number)
            }, status=status.HTTP_200_OK)
        
    def patch(self, request, seat_number):
        try:
            desired = int(request.query_params['desired'])
        except:
            desired = None
        if not desired or desired > 100 or desired < 1:
            return Response({
                "Type": "Fail",
                "Message": "Please enter a valid 'desired' parameter."
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            seat = models.Ticket.objects.get(seat_number=seat_number)
            seat.seat_number = desired
            seat.save()
        except ObjectDoesNotExist:
            return Response({
                "Type": "Fail",
                "Message": "Ticket does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        return Response({
                "Type": "Success",
                "Message": "Seat number {} is upgraded to {}.".format(seat_number, desired)
            }, status=status.HTTP_200_OK)