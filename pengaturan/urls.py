from django.urls import path
from . import views

app_name = 'pengaturan'

urlpatterns = [
    path('', views.pengaturan_view, name='settings'),
]