# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Contact(models.Model):
    user = models.ForeignKey(User, related_name='contacts')
    name = models.CharField(max_length=200, db_index=True)
    email = models.EmailField(max_length=200, unique=True)
    age = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)


