from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from .models import TahunAjaran
from .forms import TahunAjaranForm


@login_required
def tahun_ajaran_list(request):
    """Tampilkan daftar tahun ajaran dengan fitur pencarian."""
    search = request.GET.get('search', '')
    semester_filter = request.GET.get('semester', '')

    queryset = TahunAjaran.objects.all().order_by('-tahun', 'semester')

    if search:
        queryset = queryset.filter(
            Q(tahun__icontains=search) |
            Q(semester__icontains=search)
        )

    if semester_filter:
        queryset = queryset.filter(semester=semester_filter)

    context = {
        'tahun_ajaran_list': queryset,
        'search_query': search,
        'semester_filter': semester_filter,
        'form': TahunAjaranForm(),
        'total_count': TahunAjaran.objects.count(),
    }
    return render(request, 'akademik/tahun_ajaran_list.html', context)


@login_required
def tahun_ajaran_create(request):
    """Tambah data tahun ajaran baru."""
    if request.method == 'POST':
        form = TahunAjaranForm(request.POST)
        if form.is_valid():
            try:
                # Jika is_aktif = True, nonaktifkan yang lain
                if form.cleaned_data.get('is_aktif'):
                    TahunAjaran.objects.filter(is_aktif=True).update(is_aktif=False)
                form.save()
                messages.success(request, 'Tahun ajaran berhasil ditambahkan.')
            except IntegrityError:
                messages.error(request, 'Kombinasi tahun dan semester sudah ada.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    return redirect('akademik:tahun_ajaran_list')


@login_required
def tahun_ajaran_update(request, pk):
    """Perbarui data tahun ajaran."""
    obj = get_object_or_404(TahunAjaran, pk=pk)
    if request.method == 'POST':
        form = TahunAjaranForm(request.POST, instance=obj)
        if form.is_valid():
            try:
                # Jika is_aktif = True, nonaktifkan yang lain terlebih dahulu
                if form.cleaned_data.get('is_aktif'):
                    TahunAjaran.objects.filter(is_aktif=True).exclude(pk=pk).update(is_aktif=False)
                form.save()
                messages.success(request, 'Tahun ajaran berhasil diperbarui.')
            except IntegrityError:
                messages.error(request, 'Kombinasi tahun dan semester sudah ada.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    return redirect('akademik:tahun_ajaran_list')


@login_required
def tahun_ajaran_delete(request, pk):
    """Hapus data tahun ajaran."""
    obj = get_object_or_404(TahunAjaran, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Tahun ajaran berhasil dihapus.')
    return redirect('akademik:tahun_ajaran_list')


@login_required
def tahun_ajaran_set_aktif(request, pk):
    """Set tahun ajaran tertentu sebagai aktif."""
    if request.method == 'POST':
        obj = get_object_or_404(TahunAjaran, pk=pk)
        TahunAjaran.objects.filter(is_aktif=True).update(is_aktif=False)
        obj.is_aktif = True
        obj.save()
        messages.success(request, f'{obj} berhasil diset sebagai tahun ajaran aktif.')
    return redirect('akademik:tahun_ajaran_list')
