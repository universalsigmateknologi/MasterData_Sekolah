from django.contrib import admin
from .models import PenempatanKelas, MutasiSiswa, BerkasSiswa

# Inline untuk ditampilkan di Admin Siswa (opsional, tapi bagus)
class PenempatanKelasInline(admin.TabularInline):
    model = PenempatanKelas
    extra = 0
    readonly_fields = ('created_at',)

class MutasiSiswaInline(admin.TabularInline):
    model = MutasiSiswa
    extra = 0

class BerkasSiswaInline(admin.TabularInline):
    model = BerkasSiswa
    extra = 0

# Registrasi Admin Masing-Masing Model
@admin.register(PenempatanKelas)
class PenempatanKelasAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'kelas', 'tahun_ajaran', 'keterangan')
    list_filter = ('tahun_ajaran', 'kelas')
    search_fields = ('siswa__nama_lengkap',)

@admin.register(MutasiSiswa)
class MutasiSiswaAdmin(admin.ModelAdmin):
    list_display = ('jenis_mutasi', 'siswa', 'tanggal_mutasi')
    list_filter = ('jenis_mutasi',)

@admin.register(BerkasSiswa)
class BerkasSiswaAdmin(admin.ModelAdmin):
    list_display = ('nama_berkas', 'siswa', 'created_at')
    list_filter = ('nama_berkas',)
    search_fields = ('siswa__nama_lengkap',)