from .models import Pengaturan

def pengaturan_global(request):
    # Mengambil data pengaturan pertama, atau None jika belum ada data
    pengaturan = Pengaturan.objects.first()
    
    # Mengembalikan data dalam bentuk dictionary agar bisa diakses di template
    return {
        'global_pengaturan': pengaturan
    }