from account import models
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.UserModel
        fields = ['username', 'password', 'last_login']

    def create(self, validated_data):
        user = models.UserModel(
            username=validated_data['username'],
            password=validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()
        profile = models.UserProfile(user=user, last_request=now())
        profile.save()

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        user.last_login = now()
        user.save()

        return token
