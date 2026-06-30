from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Pengaturan
from .forms import PengaturanForm

def pengaturan_view(request):
    # Ambil instance yang ada, atau None jika belum ada data sama sekali
    instance = Pengaturan.objects.first()
    
    if request.method == 'POST':
        # Jika instance None, Django akan otomatis membuat objek baru saat form.save()
        form = PengaturanForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pengaturan berhasil disimpan.')
            return redirect('pengaturan:settings')
    else:
        form = PengaturanForm(instance=instance)

    context = {
        'form': form,
        'instance': instance, # Dikirim untuk menampilkan preview logo lama
    }
    return render(request, 'pengaturan/pengaturan_form.html', context)