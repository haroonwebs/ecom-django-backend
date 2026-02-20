from .utils import Utils
from rest_framework import serializers
from accounts.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes, smart_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta: 
        model= User
        fields= ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {"write_only": True}
        }
    
    # validate password2 and password2 
    def validate(self, attrs):
        passwrod= attrs.get('password')
        passwrod2= attrs.get('password2')
        if passwrod != passwrod2:
            raise serializers.ValidationError("password and confirm passord not match")
        return attrs
    
    # create user 
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields= ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'name', 'email']



class UpdateUserPasswordSerializer(serializers.Serializer):
    password= serializers.CharField(max_length=255, style={"input_type": "password"}, write_only=True)
    password2= serializers.CharField(max_length=255, style={"input_type": "password"}, write_only=True)

    class Meta:
        model= User
        fields=[ 'password', 'password2']

    def validate(self, attrs):
        password= attrs.get('password')
        password2= attrs.get('password2')
        user= self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("password and confirm passord not match")
        user.set_password(password)
        user.save()
        return attrs      
    


class SendResetPasswordEmailSerializer(serializers.Serializer):
    email= serializers.EmailField(max_length=255)
    class Meta:
        model= User
        fields=['email']


    def validate(self, attrs):
        email= attrs.get('email')
        if User.objects.filter(email=email).exists():
            user= User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token= PasswordResetTokenGenerator().make_token(user=user)
            link='http://localhost:3000/api/user/sent-rest-password-email/'+uid+'/'+token
            print("link", link )
            # send email function call
            data={
                'subject': 'Reset Your Password',
                'body': f"Click link to reset password: {link}",
                'to_email': user.email
            }

            Utils.send_email(data)
        else:    
            raise serializers.ValidationError("User with this email does not exist")
        return attrs    



class ResetPasswordSerializer(serializers.Serializer):
    password= serializers.CharField(max_length=255, style={"input_type": "password"}, write_only=True)
    password2= serializers.CharField(max_length=255, style={"input_type": "password"}, write_only=True)

    class Meta:
        model= User
        fields=['password', 'password2']


    def validate(self, attrs):
       try:
        password= attrs.get('password')
        password2= attrs.get('password2')
        uid= self.context.get('uid')
        token= self.context.get('token')
        if password != password2:
            raise serializers.ValidationError("password and confirm passord not match")
        id= smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user=user, token=token):
            raise serializers.ValidationError('User and token not match')
        user.set_password(password)
        user.save()
        return attrs   
       except DjangoUnicodeDecodeError as identifier:
           PasswordResetTokenGenerator().check_token(user=user, token=token)
           raise serializers.ValidationError("token is not valid or expire")