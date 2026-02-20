from rest_framework import serializers
from accounts.models import User


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