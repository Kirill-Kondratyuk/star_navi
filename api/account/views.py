from django.http import Http404
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from account import serializers


UserModel = get_user_model()


class UserSignup(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token_string = request.data.get('refresh')
        access_token_string = request.data.get('access')

        if not refresh_token_string:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            access_token = AccessToken(access_token_string)
            access_token.set_exp(now())

            refresh_token = RefreshToken(refresh_token_string)
            refresh_token.blacklist()
        except TokenError:
            pass

        return Response(status=status.HTTP_200_OK)


class UserLogin(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer
