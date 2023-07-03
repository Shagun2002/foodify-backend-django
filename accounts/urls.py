from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
)

from .views import MyTokenObtainPairView

urlpatterns = [
    # path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # custom token pair view for obtaining custom access token
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", register_api, name="register_api"),
    path("get-user-data/", get_user_data, name="get_user_data"),
    
    path("reset-password/", PasswordResetView.as_view(), name="reset_password"),
]
