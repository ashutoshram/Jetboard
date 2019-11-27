from django.conf.urls import url
from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    path('room_stats/<str:room>', views.room_stats, name='room_stats'),
    url(r'^refreshRoomStats/$', views.refreshRoomStats, name="refreshRoomStats"),
    url(r'^refreshHomeTable/$', views.refreshHomeTable, name="refreshHomeTable"),
]
