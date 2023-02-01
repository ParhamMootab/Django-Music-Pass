from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from .models import User
from MusicPass.settings import JWT_SECRET_KEY

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization = request.META.get("HTTP_AUTHORIZATION")
        
        try:
            authorization_list = authorization.split(" ") # raises attribute error if no token
            if not authorization_list or authorization_list[0].lower() != 'bearer' or len(authorization_list) == 1:
                return None
            token = authorization_list[1]
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(email=payload['id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        except AttributeError:
            return None # user can access safe methods (Readonly)
        except:
            raise AuthenticationFailed('Invalid token')
        
        return (user, token)
        