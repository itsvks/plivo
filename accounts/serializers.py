# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")
        read_only_fields = ("id",)
        write_only_fields = ("password",)

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )

        user.set_password(validated_data["password"])
        user.save()

        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)
        return super(RegisterSerializer, self).update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=128)


class TokenSerializer(serializers.Serializer):
    class Meta:
        model = Token
        fields = ("key",)
