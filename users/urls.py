from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # 회원가입 / 로그인, 로그아웃
    path('signup', views.JWTSignupView.as_view()),
    path('login', views.JWTLoginView.as_view()),
    # path('logout', views.JWTLogoutView.as_view()),
    # 토큰 재발급하기
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
