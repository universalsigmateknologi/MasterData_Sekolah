from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q, Count
from .models import TahunAjaran, Jurusan, Kelas
from .forms import TahunAjaranForm, JurusanForm, KelasForm


# ─────────────────────────── TAHUN AJARAN ───────────────────────────

@login_required
def tahun_ajaran_list(request):
    search = request.GET.get('search', '')
    semester_filter = request.GET.get('semester', '')

    queryset = TahunAjaran.objects.all().order_by('-tahun', 'semester')

    if search:
        queryset = queryset.filter(
            Q(tahun__icontains=search) | Q(semester__icontains=search)
        )
    if semester_filter:
        queryset = queryset.filter(semester=semester_filter)

    return render(request, 'akademik/tahun_ajaran_list.html', {
        'tahun_ajaran_list': queryset,
        'search_query': search,
        'semester_filter': semester_filter,
        'form': TahunAjaranForm(),
        'total_count': TahunAjaran.objects.count(),
    })


@login_required
def tahun_ajaran_create(request):
    if request.method == 'POST':
        form = TahunAjaranForm(request.POST)
        if form.is_valid():
            try:
                if form.cleaned_data.get('is_aktif'):
                    TahunAjaran.objects.filter(is_aktif=True).update(is_aktif=False)
                form.save()
                messages.success(request, 'Tahun ajaran berhasil ditambahkan.')
            except IntegrityError:
                messages.error(request, 'Kombinasi tahun dan semester sudah ada.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    return redirect('akademik:tahun_ajaran_list')


@login_required
def tahun_ajaran_update(request, pk):
    obj = get_object_or_404(TahunAjaran, pk=pk)
    if request.method == 'POST':
        form = TahunAjaranForm(request.POST, instance=obj)
        if form.is_valid():
            try:
                if form.cleaned_data.get('is_aktif'):
                    TahunAjaran.objects.filter(is_aktif=True).exclude(pk=pk).update(is_aktif=False)
                form.save()
                messages.success(request, 'Tahun ajaran berhasil diperbarui.')
            except IntegrityError:
                messages.error(request, 'Kombinasi tahun dan semester sudah ada.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    return redirect('akademik:tahun_ajaran_list')


@login_required
def tahun_ajaran_delete(request, pk):
    obj = get_object_or_404(TahunAjaran, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Tahun ajaran berhasil dihapus.')
    return redirect('akademik:tahun_ajaran_list')


@login_required
def tahun_ajaran_set_aktif(request, pk):
    if request.method == 'POST':
        obj = get_object_or_404(TahunAjaran, pk=pk)
        TahunAjaran.objects.filter(is_aktif=True).update(is_aktif=False)
        obj.is_aktif = True
        obj.save()
        messages.success(request, f'{obj} berhasil diset sebagai tahun ajaran aktif.')
    return redirect('akademik:tahun_ajaran_list')


# ─────────────────────────── JURUSAN ───────────────────────────

@login_required
def jurusan_list(request):
    search = request.GET.get('search', '')
    queryset = Jurusan.objects.annotate(jumlah_kelas=Count('kelas')).order_by('kode_jurusan')

    if search:
        queryset = queryset.filter(
            Q(nama_jurusan__icontains=search) | Q(kode_jurusan__icontains=search)
        )

    return render(request, 'akademik/jurusan_list.html', {
        'jurusan_list': queryset,
        'search_query': search,
        'total_count': Jurusan.objects.count(),
    })


@login_required
def jurusan_create(request):
    if request.method == 'POST':
        form = JurusanForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Jurusan berhasil ditambahkan.')
            except IntegrityError:
                messages.error(request, 'Kode jurusan sudah digunakan.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    return redirect('akademik:jurusan_list')


@login_required
def jurusan_update(request, pk):
    obj = get_object_or_404(Jurusan, pk=pk)
    if request.method == 'POST':
        form = JurusanForm(request.POST, instance=obj)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Jurusan berhasil diperbarui.')
            except IntegrityError:
                messages.error(request, 'Kode jurusan sudah digunakan.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    return redirect('akademik:jurusan_list')


@login_required
def jurusan_delete(request, pk):
    obj = get_object_or_404(Jurusan, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Jurusan berhasil dihapus.')
    return redirect('akademik:jurusan_list')


# ─────────────────────────── KELAS ───────────────────────────

@login_required
def kelas_list(request):
    search = request.GET.get('search', '')
    tingkat_filter = request.GET.get('tingkat', '')
    jurusan_filter = request.GET.get('jurusan', '')

    queryset = Kelas.objects.select_related('jurusan').order_by('tingkat', 'nama_kelas')

    if search:
        queryset = queryset.filter(
            Q(nama_kelas__icontains=search) |
            Q(jurusan__nama_jurusan__icontains=search) |
            Q(jurusan__kode_jurusan__icontains=search)
        )
    if tingkat_filter:
        queryset = queryset.filter(tingkat=tingkat_filter)
    if jurusan_filter:
        queryset = queryset.filter(jurusan__id=jurusan_filter)

    return render(request, 'akademik/kelas_list.html', {
        'kelas_list': queryset,
        'search_query': search,
        'tingkat_filter': tingkat_filter,
        'jurusan_filter': jurusan_filter,
        'jurusan_choices': Jurusan.objects.order_by('kode_jurusan'),
        'total_count': Kelas.objects.count(),
        'form': KelasForm(),
    })


@login_required
def kelas_create(request):
    if request.method == 'POST':
        form = KelasForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kelas berhasil ditambahkan.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    return redirect('akademik:kelas_list')


@login_required
def kelas_update(request, pk):
    obj = get_object_or_404(Kelas, pk=pk)
    if request.method == 'POST':
        form = KelasForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kelas berhasil diperbarui.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    return redirect('akademik:kelas_list')


@login_required
def kelas_delete(request, pk):
    obj = get_object_or_404(Kelas, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Kelas berhasil dihapus.')
    return redirect('akademik:kelas_list')
