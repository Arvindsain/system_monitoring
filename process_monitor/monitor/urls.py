from django.contrib import admin
from django.urls import path
from monitor.views import ReceiveProcessData, RetrieveProcessData, RetrieveHosts

urlpatterns = [
    path('receive/', ReceiveProcessData.as_view()),
    path('hosts/', RetrieveHosts.as_view()),
    path('retrieve/<str:hostname>/', RetrieveProcessData.as_view()),
]