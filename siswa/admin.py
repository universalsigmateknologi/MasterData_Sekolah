from django.contrib import admin
from .models import Siswa, DataOrangTua

class DataOrangTuaInline(admin.StackedInline):
    model = DataOrangTua
    can_delete = False
    verbose_name_plural = 'Data Orang Tua'

@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('nisn', 'nama_lengkap', 'jenis_kelamin', 'status_siswa')
    list_filter = ('status_siswa', 'jenis_kelamin')
    search_fields = ('nama_lengkap', 'nisn', 'nik')
    
    fieldsets = (
        (None, {'fields': ('nisn', 'nik', 'nama_lengkap', 'jenis_kelamin')}),
        ('Kelahiran', {'fields': ('tempat_lahir', 'tanggal_lahir')}),
        ('Detail', {'fields': ('agama', 'golongan_darah', 'catatan_medis', 'alamat_tinggal')}),
        ('Status Akademik', {'fields': ('status_siswa', 'tanggal_masuk', 'tanggal_keluar')}),
        ('Foto', {'fields': ('foto_masuk', 'foto_keluar')}),
    )
    
    inlines = [DataOrangTuaInline]