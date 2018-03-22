# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.models import User

from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from contact.models import Contact


class ContactViewTestCase(APITestCase):
    url = reverse("contact:contact-list")

    def setUp(self):
        self.username = "vikas.shil"
        self.email = "vikas.shil@plivo.com"
        self.password = "vikas@12345"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_contact(self):
        response = self.client.post(self.url, {"name": "Niraj", "email": "niraj@plivo.com", "age": "27",
                                               "mobile": "9876678909", "address": "Gurgaon"})
        self.assertEqual(201, response.status_code)

    def test_user_contact(self):

        Contact.objects.create(user=self.user, name="Niraj", email="niraj@plivo.com", age="27",
                               mobile="9876678909", address="Gurgaon")
        response = self.client.get(self.url + "?format=json")
        self.assertTrue(json.loads(response.content)["count"] == Contact.objects.count())
