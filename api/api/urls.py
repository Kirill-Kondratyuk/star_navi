from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

from account import views as auth_views
from blog import views as blog_views


BASIC_URL_PREFIX = 'api'
AUTH_URL_PREFIX = 'auth'
BLOG_URL_PREFIX = 'blog'

basic_url_patterns = [

]

auth_url_patterns = [
    path(
        route=f'{BASIC_URL_PREFIX}/{AUTH_URL_PREFIX}/token/',
        view=auth_views.UserLogin.as_view(),
        name='token_obtain_pair'
    ),
    path(
        route=f'{BASIC_URL_PREFIX}/{AUTH_URL_PREFIX}/token/refresh/',
        view=TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        route=f'{BASIC_URL_PREFIX}/{AUTH_URL_PREFIX}/signup/',
        view=auth_views.UserSignup.as_view(),
        name='signup'
    ),
    path(
        route=f'{BASIC_URL_PREFIX}/{AUTH_URL_PREFIX}/logout/',
        view=auth_views.UserLogout.as_view(),
        name='logout'
    )
]


blog_url_patterns = [
    path(
        route=f'{BASIC_URL_PREFIX}/{BLOG_URL_PREFIX}/posts/',
        view=blog_views.PostList.as_view(),
        name='posts'
    ),
    path(
        route=f'{BASIC_URL_PREFIX}/{BLOG_URL_PREFIX}/users/',
        view=blog_views.UserList.as_view(),
        name='users'
    ),
    path(
        route=f'{BASIC_URL_PREFIX}/{BLOG_URL_PREFIX}/posts/<int:pk>/like/',
        view=blog_views.PostLike.as_view(),
        name='post_like'
    ),
    path(
        route=f'{BASIC_URL_PREFIX}/{BLOG_URL_PREFIX}/users/<int:pk>/activity/',
        view=blog_views.UserActivity.as_view(),
        name='user_activity'
    ),
    path(
        route=f'{BASIC_URL_PREFIX}/{BLOG_URL_PREFIX}/analytics/',
        view=blog_views.LikesAnalytics.as_view(),
        name='likes_analytics'
    )
]

urlpatterns = basic_url_patterns \
              + auth_url_patterns \
              + blog_url_patterns
