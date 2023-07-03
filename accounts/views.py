from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *


# for customising token claims
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email
        token["role"] = user.role

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Register API
@api_view(["POST"])
def register_api(request):
    print("request.data = ", request.data)
    serializer = RegisterSerializer(data=request.data)
    # raise_exception=True is done for getting proper exception error when we enter invalid data
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    # when we create a token we get two things: created and token
    # _, token = AuthToken.objects.create(user)

    # if User.objects.filter(email=self.cleaned_data['email']).exists():
    #     return Response(
    #     {
    #         "status": status.HTTP_208_ALREADY_REPORTED,
    #         "message": "User is not authenticated!",
    #     },
    #     status=status.HTTP_208_ALREADY_REPORTED
    # )

    return Response(
        {
            "status": status.HTTP_201_CREATED,
            "user_info": serializer.data,
        },
        status=status.HTTP_201_CREATED,
    )



@api_view(["GET"])
def get_user_data(request):
    user = request.user
    if user.is_authenticated:
        return Response(
            {
                "status": status.HTTP_200_OK,
                "user_info": {
                    "id": user.id,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )
    return Response(
        {
            "status": status.HTTP_401_UNAUTHORIZED,
            "message": "User is not authenticated!",
        },
        status=status.HTTP_401_UNAUTHORIZED,
    )

    

class PasswordResetView(APIView):
    """
    An endpoint for changing password.
    """
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
        
    def put(self, request):
        user = request.user
        try:
            user = CustomUser.objects.get(email=user)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Check old password
        old_password = request.data.get("old_password")
        if not user.check_password(old_password):
            return Response(
                {"old_password": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST
            )

        # set_password also hashes the password that the user will get
        new_password = request.data.get("new_password")
        user.set_password(new_password)
        user.save()
        return Response(
            {"success": "Password reset successful"}, status=status.HTTP_200_OK
        )
