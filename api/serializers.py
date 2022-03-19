from email.policy import default
from .models import User, Appointment
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

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
    # doctor = serializers.PrimaryKeyRelatedField(read_only=True)
    # patient = serializers.PrimaryKeyRelatedField(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(read_only=True)
    description = serializers.CharField(max_length=100)


    class Meta:
        model = Appointment
        fields = (
            'id', 
            'doctor_id', 
            'patient_id', 
            'description',
        )

    def create(self, validated_data):
        # doctor_key = validated_data.pop("doctor")
        # patient_key = validated_data.pop("patient")
        print(validated_data)
        appointment = Appointment.objects.create(**validated_data)
        return appointment
