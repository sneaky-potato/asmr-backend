# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import exceptions

from .permissions import (
    IsAuthenticatedOrPostOnly,
)

from .serializers import (
    UserRegistrationSerializer,
    UserDoctorSerializer,
    UserPatientSerializer,
    UserLoginSerializer,
    UserListSerializer,
    HospitalListSerializer,
    AppointmentListSerializer,
)

from .models import (
    User, 
    Appointment,
    Hospital,
)

class AuthUserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        role = request.data['role']
        if(role == 3):
            serializer = UserPatientSerializer(data=request.data)

        elif(role == 2):
            request.data['is_active'] = False
            serializer = UserDoctorSerializer(data=request.data)
        else:
            serializer = UserRegistrationSerializer(data=request.data)

        print("requested data =", request.data)

        valid = serializer.is_valid(raise_exception=True)
        print("request is =", valid)
        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)

class AuthUserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (IsAuthenticatedOrPostOnly, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)    

class UserListView(APIView):
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role != 1:
            users = User.objects.all().filter(role=2)
            serializer = self.serializer_class(users, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched doctors',
                'users': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)
            
        else:
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched all users',
                'users': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)

    def put(self, request, pk):
        print("Entering views put request")
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise exceptions.NotFound("User does not exist", code=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(user, data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        print("request is =", valid)
        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully edited',
                'user': serializer.data
            }

            return Response(response, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HospitalListView(APIView):
    serializer_class = HospitalListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request):
        hospitals = Hospital.objects.all()
        serializer = self.serializer_class(hospitals, many=True)
        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'Successfully fetched hospitals',
            'hospitals': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        print("Entering views post request")

        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED


            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Hospital successfully registered!',
                'appointment': serializer.data
            }

            return Response(response, status=status_code)


class AppointmentListView(APIView):
    serializer_class = AppointmentListSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        print("Entering view get request")
        appointments = Appointment.objects.all()
        serializer = self.serializer_class(appointments, many=True)
        status_code = status.HTTP_200_OK

        response = {
                'success': True,
                'status_code': status_code,
                'message': 'Successfully fetched appointments',
                'appointments': serializer.data
        }
        return Response(response, status=status_code)

    def post(self, request):
        print("Entering views post request")

        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED


            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Appointment successfully registered!',
                'appointment': serializer.data
            }

            return Response(response, status=status_code)

    def put(self, request, pk):
        print("Entering views put request")
        user = request.user

        if user.role == 3:
            return Response("You do not have the permission to edit an appointment", status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise exceptions.NotFound("Appointment does not exist", code=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(appointment, data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Appointment successfully edited',
                'appointment': serializer.data
            }

            return Response(response, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
