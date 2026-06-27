from django.urls import path
from . import views

app_name = 'kesiswaan'

urlpatterns = [
    # ... url lainnya jika ada ...
    path('', views.penempatan_kelas_list, name='penempatan_kelas_list'),
    path('mutasi/', views.mutasi_siswa_list, name='mutasi_list'),
]