# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from contact.models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'user')

admin.site.register(Contact, ContactAdmin)
