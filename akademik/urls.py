from django.urls import path
from . import views

app_name = 'akademik'

urlpatterns = [
    # Tahun Ajaran
    path('tahun-ajaran/', views.tahun_ajaran_list, name='tahun_ajaran_list'),
    path('tahun-ajaran/tambah/', views.tahun_ajaran_create, name='tahun_ajaran_create'),
    path('tahun-ajaran/<int:pk>/edit/', views.tahun_ajaran_update, name='tahun_ajaran_update'),
    path('tahun-ajaran/<int:pk>/hapus/', views.tahun_ajaran_delete, name='tahun_ajaran_delete'),
    path('tahun-ajaran/<int:pk>/aktifkan/', views.tahun_ajaran_set_aktif, name='tahun_ajaran_set_aktif'),

    # Jurusan
    path('jurusan/', views.jurusan_list, name='jurusan_list'),
    path('jurusan/tambah/', views.jurusan_create, name='jurusan_create'),
    path('jurusan/<int:pk>/edit/', views.jurusan_update, name='jurusan_update'),
    path('jurusan/<int:pk>/hapus/', views.jurusan_delete, name='jurusan_delete'),

    # Kelas
    path('kelas/', views.kelas_list, name='kelas_list'),
    path('kelas/tambah/', views.kelas_create, name='kelas_create'),
    path('kelas/<int:pk>/edit/', views.kelas_update, name='kelas_update'),
    path('kelas/<int:pk>/hapus/', views.kelas_delete, name='kelas_delete'),
]
