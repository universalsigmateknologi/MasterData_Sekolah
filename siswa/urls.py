from django.urls import path
from .views import SiswaListView, SiswaCreateView, SiswaUpdateView, SiswaDeleteView, export_siswa_excel
from .views_import import SiswaImportView, download_template
from .views_detail import SiswaDetailView, DokumenSiswaCreateView, DokumenSiswaUpdateView, DokumenSiswaDeleteView

app_name = 'siswa'

urlpatterns = [
    path('', SiswaListView.as_view(), name='index'),
    path('tambah/', SiswaCreateView.as_view(), name='create'),
    path('import/', SiswaImportView.as_view(), name='import'),
    path('download-template/', download_template, name='download_template'),
    path('export/', export_siswa_excel, name='export_excel'),
    path('<int:pk>/', SiswaDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', SiswaUpdateView.as_view(), name='update'),
    path('<int:pk>/hapus/', SiswaDeleteView.as_view(), name='delete'),
    path('<int:pk>/dokumen/tambah/', DokumenSiswaCreateView.as_view(), name='dokumen_create'),
    path('<int:pk>/dokumen/<int:dokumen_id>/edit/', DokumenSiswaUpdateView.as_view(), name='dokumen_update'),
    path('<int:pk>/dokumen/<int:dokumen_id>/hapus/', DokumenSiswaDeleteView.as_view(), name='dokumen_delete'),
]