# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from contact.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'email', 'mobile', 'age', 'address')
