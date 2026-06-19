from django.urls import path
from .views import SiswaListView, SiswaCreateView, SiswaUpdateView, SiswaDeleteView
from .views_import import SiswaImportView, download_template

app_name = 'siswa'

urlpatterns = [
    path('', SiswaListView.as_view(), name='index'),
    path('tambah/', SiswaCreateView.as_view(), name='create'),
    path('import/', SiswaImportView.as_view(), name='import'),
    path('download-template/', download_template, name='download_template'),
    path('<int:pk>/edit/', SiswaUpdateView.as_view(), name='update'),
    path('<int:pk>/hapus/', SiswaDeleteView.as_view(), name='delete'),
]