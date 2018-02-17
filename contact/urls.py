from django.conf.urls import url

from contact import views


urlpatterns = [
    url(r'^$', views.ContactView.as_view(), name='contact-list'),
    url(r'^(?P<pk>[0-9]+)/$', views.ContactDetailView.as_view(), name='contact-detail'),

]
