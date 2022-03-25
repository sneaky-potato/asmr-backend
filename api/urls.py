from django.urls import path
from api.serializers import DoctorListAdminSerializer, DoctorListSerializer
from rest_framework_simplejwt import views as jwt_views

from .views import (
    AuthUserRegistrationView,
    AuthUserLoginView,
    DoctorListView,
    # Ping,
    MeView,
    UserEditView,
    # UserListView,
    HospitalListView,
    AppointmentListView,
)   

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register', AuthUserRegistrationView.as_view(), name='register'),
    path('login', AuthUserLoginView.as_view(), name='login'),

    # path('ping', Ping.as_view(), name='ping'),
    path('me', MeView.as_view(), name='me'),

    path('doctors', DoctorListView.as_view(), name='users'),
    path('users/<int:pk>/', UserEditView.as_view(), name='update user'),
    path('appointments', AppointmentListView.as_view(), name='appointments'),
    path('appointments/<int:pk>/', AppointmentListView.as_view(), name='appointment'),
    path('hospitals', HospitalListView.as_view(), name='hospitals'),
]