from django.contrib import admin
from .models import TahunAjaran, Jurusan, Kelas

@admin.register(TahunAjaran)
class TahunAjaranAdmin(admin.ModelAdmin):
    list_display = ('tahun', 'semester', 'is_aktif')
    list_filter = ('is_aktif', 'semester')

@admin.register(Jurusan)
class JurusanAdmin(admin.ModelAdmin):
    list_display = ('kode_jurusan', 'nama_jurusan')

@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ('nama_kelas', 'tingkat', 'jurusan')
    list_filter = ('tingkat', 'jurusan')