# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import LoginSerializer, RegisterSerializer, TokenSerializer


class RegisterView(generics.CreateAPIView):
    """
        Register a new user to system
    """

    serializer_class = RegisterSerializer
    model = User

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            if user:
                login(request, user, backend='accounts.backends.EmailAuthBackEnd')

                token = Token.objects.get_or_create(user=user)[0].key

                return Response(
                    {
                        'token': token,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    },
                    status=status.HTTP_200_OK
                )

        else:
            return Response(
                {
                    'user': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    """
        Login a existing user to system
    """
    serializer_class = LoginSerializer
    token_model = Token

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = authenticate(email=serializer.data['email'], password=serializer.data['password'])
            if user and user.is_authenticated():
                if user.is_active:
                    login(request, user)

                    token = self.token_model.objects.get_or_create(user=user)[0].key

                    # Update last login time
                    user.last_login = timezone.now()
                    user.save(update_fields=['last_login'])

                    return Response({
                        'token': token,
                        'first_name': user.first_name,
                        'last_name': user.last_name},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response({
                        'error': ['This account is disabled.']},
                         status=status.HTTP_401_UNAUTHORIZED
                    )
            else:
                return Response({
                    'error': ['Invalid Username/Password.']},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
        Logout a logged in user to system
    """

    def get(self, request):
        try:
            logout(request)
            return Response({
                'success': 'Successfully logged out.'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            pass
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
