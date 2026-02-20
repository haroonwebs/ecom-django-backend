from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserProfileSerializer, UpdateUserPasswordSerializer, SendResetPasswordEmailSerializer, ResetPasswordSerializer
from django.contrib.auth import authenticate
from accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

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
                     if user is not None:
                            token= get_tokens_for_user(user=user)
                            return Response({
                                   'message': 'User Login Successfully',
                                   'data': serializer.data,
                                   'token': token
                            }, status=status.HTTP_200_OK)
                     else:
                      return Response(
                            {'errors':{'non_field_errors':['Email or Password in not valid']}},
                              status=status.HTTP_404_NOT_FOUND)
                     
              return Response( serializer.errors ,status=status.HTTP_404_NOT_FOUND)       
                     

# get user profile     
class UserProfileView(APIView):
       renderer_classes=[UserRenderer]
       permission_classes=[IsAuthenticated]
       def get(self, request, format=None):
             serializer= UserProfileSerializer(request.user)
             return Response({'data': serializer.data}, status=status.HTTP_200_OK)



class UpdateUserPasswordView(APIView):
       permission_classes=[IsAuthenticated]
       renderer_classes=[UserRenderer]
       def patch(self, request, format=None):
             print('data', request.data)
             serializer= UpdateUserPasswordSerializer(data=request.data, context={'user': request.user})
             if serializer.is_valid(raise_exception=True):
                   return Response({'message': "Password Updated Successfuly"}, status=status.HTTP_200_OK)
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       


class SendResetPasswordEmailView(APIView):
      def post(self, request, format=None):
            serializer=SendResetPasswordEmailSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                  return Response({'message':'Passwrod reset email is delivered, Please check your inbox'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ResetPasswordView(APIView):
      def post(self, request, uid, token, format=None):
            serializer=ResetPasswordSerializer(data=request.data, context={'uid':uid, 'token':token})
            if serializer.is_valid(raise_exception=True):
                  return Response({'message':'Your password reset successfully'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                            