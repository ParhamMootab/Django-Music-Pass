from rest_framework.views import APIView
from .models import User
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
import jwt, datetime
from MusicPass.settings import JWT_SECRET_KEY


# Create your views here.
class RegisterAPI(APIView):
    
    def post(self, request):
        deserialized_data = UserSerializer(data=request.data)
        if deserialized_data.is_valid():
            deserialized_data.save()
            return Response({
                "Type": "Success",
                "Message": "You have successfully signed up to MusicPass"
            }, status=status.HTTP_201_CREATED)
            
        else:
            return Response({
                "Type": "Fail",
                "Message": deserialized_data.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
class LoginAPI(APIView):
    
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({
                "Type": "Fail",
                "Message": "User does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
            return Response({
                "Type": "Fail",
                "Message": "Wrong Password"
            }, status=status.HTTP_404_NOT_FOUND)
        
        payload = {
            'id': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
                         
        token = jwt.encode(payload, JWT_SECRET_KEY , algorithm='HS256')
        response = Response({
                "Type": "Success",
                "Message": "Logged in to MusicPass successfully."
            }, status=status.HTTP_200_OK)
        response.set_cookie('jwt', token, httponly=True)
        return response
    
        
        