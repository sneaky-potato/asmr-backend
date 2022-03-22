from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    AuthUserRegistrationView,
    AuthUserLoginView,
    UserListView,
    HospitalListView,
    AppointmentListView,
)

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register', AuthUserRegistrationView.as_view(), name='register'),
    path('login', AuthUserLoginView.as_view(), name='login'),
    path('users', UserListView.as_view(), name='users'),
    path('users/<int:pk>/', UserListView.as_view(), name='update user'),
    path('appointments', AppointmentListView.as_view(), name='appointments'),
    path('appointments/<int:pk>/', AppointmentListView.as_view(), name='appointment'),
    path('hospitals', HospitalListView.as_view(), name='hospitals'),
]