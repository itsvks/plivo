# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from rest_framework import filters
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from contact.models import Contact
from contact.serializers import ContactSerializer


class ContactView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    model = Contact
    serializer_class = ContactSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')

    def get_queryset(self):
        user = self.request.user
        return self.model.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    model = Contact
    serializer_class = ContactSerializer

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
