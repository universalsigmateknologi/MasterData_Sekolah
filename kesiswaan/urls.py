from django.urls import path
from . import views

app_name = 'kesiswaan'

urlpatterns = [
    # ... url lainnya jika ada ...
    path('', views.penempatan_kelas_list, name='penempatan_kelas_list'),
    path('kenaikan-kelas/', views.kenaikan_kelas_view, name='kenaikan_kelas'), # Route Baru
    path('mutasi/', views.mutasi_siswa_list, name='mutasi_list'),
    path('mutasi/tambah/', views.mutasi_create, name='mutasi_create'),
]