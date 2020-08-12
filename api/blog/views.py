from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
    IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from blog import models as blog_models
from blog import serializers as blog_serializers
from account import models as account_models
from account import serializers as account_serializers
from blog.utils import validate_date_query_params


class UserList(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = account_serializers.UserSerializer
    queryset = account_models.get_user_model().objects.all()


class PostList(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = blog_serializers.PostSerializer
    queryset = blog_models.PostModel.objects.all()
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        jwt_auth = JWTAuthentication()
        user, token = jwt_auth.authenticate(request)

        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        payload = self.request.data
        payload['likes'] = []
        payload['user'] = user.id

        serializer = blog_serializers.PostSerializer(data=payload)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostLike(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_post(pk):
        try:
            post = blog_models.PostModel.objects.get(id=pk)
        except blog_models.PostModel.DoesNotExist:
            raise Http404
        return post

    @staticmethod
    def get_like(**kwargs):
        try:
            like = blog_models.LikeModel.objects.get(**kwargs)
        except blog_models.LikeModel.DoesNotExist:
            raise Http404
        return like

    def post(self, request, pk):
        post = self.get_post(pk=pk)
        try:
            blog_models.LikeModel.objects.get(post=post, user=request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except blog_models.LikeModel.DoesNotExist:
            like = blog_models.LikeModel(post=post, user=request.user)
            like.save()
        data = {
            'message': f'Post {post.id} was liked by user {request.user.username}'
        }
        return Response(data=data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        post = self.get_post(pk=pk)
        search_params = {
            'user': request.user,
            'post': post
        }
        like = self.get_like(**search_params)
        print(like)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserActivity(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get_object(pk):
        try:
            user = account_models.UserModel.objects.get(id=pk)
        except account_models.UserModel.DoesNotExists:
            raise Http404
        return user

    def get(self, request, pk):
        user = self.get_object(pk=pk)
        serializer = account_serializers.UserSerializer(user)
        data = serializer.data
        data['last_request'] = user.profile.last_request
        return Response(data=data, status=status.HTTP_200_OK)


class LikesAnalytics(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        date_from = request.GET.get('date_from')

        if not date_from:
            data = {
                'error': 'Missing date_from query parameter'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        date_to = request.GET.get('date_to')

        if not date_to:
            data = {
                'error': 'Missing date_to query parameter'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        validated = validate_date_query_params(date_from=date_from, date_to=date_to)
        if not validated['is_valid']:
            return Response(data=validated['errors'], status=status.HTTP_400_BAD_REQUEST)

        likes = blog_models.LikeModel.objects.filter(created__range=[date_from, date_to])
        data = {
            'likes_made': len(likes)
        }
        return Response(data=data, status=status.HTTP_200_OK)
