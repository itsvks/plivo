# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


class EmailAuthBackEnd(ModelBackend):
    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
            return None

        except User.DoesNotExist:
            return None