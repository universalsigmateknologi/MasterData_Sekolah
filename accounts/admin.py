from django.contrib import admin
from .models import Pengaturan

@admin.register(Pengaturan)
class PengaturanAdmin(admin.ModelAdmin):
    list_display = ('nama_program', 'updated_at')
    
    def has_add_permission(self, request):
        """Menyembunyikan tombol 'Tambah' jika sudah ada data"""
        if Pengaturan.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        """(Opsional) Mencegah pengaturan dihapus agar sistem tidak error"""
        return False