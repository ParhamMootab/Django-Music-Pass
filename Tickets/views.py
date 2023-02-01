from django.shortcuts import render
from rest_framework import views
from . import models, serializer
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from User.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
class TicketingAPI(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        """GET request for /ticket

        Returns:
            All the tickets or tickets from and to a specified seat number
        """
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
        """POST request for creating a new ticket

        Returns:
            Success or Failure Message
        """
        desirilized_data = serializer.TicketSerializer(data=request.data, context={'request': request})
        if desirilized_data.is_valid():
            #desirilized_data.validated_data['user_id'] = request.user['user_id']
            desirilized_data.save()
            return Response({
                "Type": "Success",
                "Message": "Your ticket for seat number {} is booked!".format(desirilized_data.validated_data.get("seat_number"))
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(desirilized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class SingleTicketAPI(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
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
            ticket_to_delete = models.Ticket.objects.get(seat_number=seat_number)
            if ticket_to_delete.user_id == request.user:
                ticket_to_delete.delete()
            else:
                return Response({
                    "message": "You are not the owner of this ticket."
                    }, status=status.HTTP_403_FORBIDDEN)
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
            if seat.user_id == request.user:
                seat.seat_number = desired
                seat.save()
            else:
                return Response({
                    "message": "You are not the owner of this ticket."
                    }, status=status.HTTP_403_FORBIDDEN)
            
        except ObjectDoesNotExist:
            return Response({
                "Type": "Fail",
                "Message": "Ticket does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        return Response({
                "Type": "Success",
                "Message": "Seat number {} is upgraded to {}.".format(seat_number, desired)
            }, status=status.HTTP_200_OK)