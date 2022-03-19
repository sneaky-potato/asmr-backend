from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from .models import (
    User, 
    Appointment,
)

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'role',
        )

    # Fucking important
    def create(self, validated_data):
        print("Entering serializer create request")
        print("validated data =", validated_data)
        auth_user = User.objects.create_user(**validated_data)
        return auth_user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'role': user.role,
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")



class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'uid',
            'email',
            'role'
        )

class AppointmentListSerializer(serializers.ModelSerializer):

    doctor_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all().filter(role=2), read_only=False)
    patient_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all().filter(role=3), read_only=False)

    class Meta:
        model = Appointment
        fields = (
            'id',
            'doctor_id', 
            'patient_id', 
            'description',
            'status',
        )

    def create(self, validated_data):
        print("Entering serializer create request")
        print("validated data =", validated_data)
        appointment = Appointment.objects.create(doctor=validated_data['doctor_id'], patient=validated_data['patient_id'], description=validated_data['description'], status=validated_data['status'])
        return appointment
