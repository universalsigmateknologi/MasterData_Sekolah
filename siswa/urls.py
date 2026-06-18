from django.urls import path
from .views import SiswaListView, SiswaCreateView, SiswaUpdateView, SiswaDeleteView

app_name = 'siswa'

urlpatterns = [
    path('', SiswaListView.as_view(), name='index'),
    path('tambah/', SiswaCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', SiswaUpdateView.as_view(), name='update'),
    path('<int:pk>/hapus/', SiswaDeleteView.as_view(), name='delete'),
]