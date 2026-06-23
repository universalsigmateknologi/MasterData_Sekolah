from django.urls import path
from . import views

app_name = 'akademik'

urlpatterns = [
    path('tahun-ajaran/', views.tahun_ajaran_list, name='tahun_ajaran_list'),
    path('tahun-ajaran/tambah/', views.tahun_ajaran_create, name='tahun_ajaran_create'),
    path('tahun-ajaran/<int:pk>/edit/', views.tahun_ajaran_update, name='tahun_ajaran_update'),
    path('tahun-ajaran/<int:pk>/hapus/', views.tahun_ajaran_delete, name='tahun_ajaran_delete'),
    path('tahun-ajaran/<int:pk>/aktifkan/', views.tahun_ajaran_set_aktif, name='tahun_ajaran_set_aktif'),
]
