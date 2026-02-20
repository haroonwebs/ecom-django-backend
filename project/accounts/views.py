from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken

# function to generate tokens 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# user RegisterUserView
class RegisterUserView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, format=None):
        print("data.req--->", request.data)
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
                    user=serializer.save()
                    token= get_tokens_for_user(user=user)
                    return Response({
                           "message":"User Register Successfully",
                           "data": serializer.data,
                           "token": token
                                     } ,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserLoginView(APIView):
       renderer_classes = [UserRenderer]
       def post(sefl, request, format=None):
              serializer= UserLoginSerializer(data=request.data)
              if serializer.is_valid(raise_exception=True):
                     
                     email= serializer.data.get('email')
                     password=serializer.data.get('password')
                     user = authenticate(email=email, password=password)
                     token= get_tokens_for_user(user=user)
                     if user is not None:
                            return Response({
                                   'message': 'User Login Successfully',
                                   'data': serializer.data,
                                   'token': token
                            }, status=status.HTTP_200_OK)
                     else:
                      return Response(
                            {'errors':{'non_field_error':['Email or Password in not valid']}},
                              status=status.HTTP_404_NOT_FOUND)
                     
              return Response( serializer.errors ,status=status.HTTP_404_NOT_FOUND)       
                     
                     