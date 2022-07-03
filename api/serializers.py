from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Appointment


# Appointment Serializer
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
    

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={"input_type":"password"},write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password','confirm_password']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        if password!=confirm_password:
            raise serializers.ValidationError({"error":"password doesn't match"})


        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':"Email already Exists"})

        
        account = User(email=self.validated_data['email'],username=self.validated_data['username'])
        account.set_password(password)
        account.save()




class ProfileUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['username','old_password','new_password','confirm_password']
    
    
