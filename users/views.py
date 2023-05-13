from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from utils.response import response
from .models import User
from .serializers import JWTSignupSerializer, JWTLoginSerializer


class JWTSignupView(APIView):
    permission_classes = [AllowAny]
    serializer_class = JWTSignupSerializer

    def post(self, request):
        """
        회원가입
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # token = TokenObtainPairSerializer.get_token(user)
            # refresh_token, access_token = str(token), str(token.access_token)
            # response = Response(
            #     {
            #         'user': serializer.data,
            #         'message': 'SUCCESS: Register',
            #         'token': {
            #             'access': access_token,
            #             'refresh': refresh_token
            #         },
            #     },
            #     status=status.HTTP_201_CREATED
            # )
            # response.set_cookie('access', access_token, httponly=True)
            # response.set_cookie('refresh', refresh_token, httponly=True)
            res = response(status=status.HTTP_201_CREATED)
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = response(status=400, message=serializer.errors)
            return Response(res, status=status.HTTP_200_OK)


class JWTLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = JWTLoginSerializer

    def post(self, request):
        """
        로그인
        로그인 성공시 access token과 refresh token 리턴
        """
        user = authenticate(
            request,
            email=request.data.get("email"),
            password=request.data.get("password"),
        )
        if not user:
            res = response(status=status.HTTP_400_BAD_REQUEST, message="이메일 또는 비밀번호를 확인하세요.")
            return Response(res, status=status.HTTP_200_OK)

        login(request, user)
        token = TokenObtainPairSerializer.get_token(user)
        # User.objects.get()
        #         serializer = LoginSerializer(user)
        res = response(status=200, data={
            "token": {
                "access": str(token.access_token),
                "refresh": str(token),
            }
        })
        return Response(res, status=status.HTTP_200_OK)
