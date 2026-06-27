from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import PenempatanKelas
from akademik.models import Kelas, TahunAjaran
from siswa.models import Siswa

def penempatan_kelas_list(request):
    if request.method == 'POST':
        selected_siswa_ids = request.POST.getlist('selected_siswa')
        target_kelas_id = request.POST.get('target_kelas')
        target_ta_id = request.POST.get('target_ta')

        if not selected_siswa_ids:
            messages.error(request, 'Pilih minimal satu siswa untuk ditempatkan.')
        elif not target_kelas_id or not target_ta_id:
            messages.error(request, 'Pilih Tahun Ajaran dan Kelas tujuan.')
        else:
            try:
                kelas = Kelas.objects.get(id=target_kelas_id)
                ta = TahunAjaran.objects.get(id=target_ta_id)
                
                # Siapkan objek untuk bulk create
                placements = [
                    PenempatanKelas(
                        siswa_id=siswa_id, 
                        kelas=kelas, 
                        tahun_ajaran=ta,
                        keterangan='Aktif'
                    ) for siswa_id in selected_siswa_ids
                ]
                # Gunakan bulk_create agar efisien dan tidak terkena unique constraint error jika ada duplikat
                PenempatanKelas.objects.bulk_create(placements, ignore_conflicts=True)
                
                messages.success(request, f'Berhasil menempatkan {len(placements)} siswa ke kelas {kelas.nama_kelas}.')
            except Exception as e:
                messages.error(request, f'Terjadi kesalahan: {str(e)}')
            
            # Redirect kembali ke URL yang sama dengan menyertakan filter GET jika ada
            return redirect(request.get_full_path())

    # ------------------- GET LOGIC -------------------
    search_query = request.GET.get('search', '')
    jk_filter = request.GET.get('jenis_kelamin', '')
    ta_filter = request.GET.get('tahun_ajaran', '')
    
    # Ambil Tahun Ajaran aktif sebagai default
    active_ta = TahunAjaran.objects.filter(is_aktif=True).first()
    if not ta_filter and active_ta:
        ta_filter = str(active_ta.id)

    # Base queryset: Hanya siswa aktif
    queryset = Siswa.objects.filter(status_siswa='Aktif').order_by('nama_lengkap')

    # Exclude siswa yang SUDAH memiliki penempatan kelas di Tahun Ajaran yang dipilih
    if ta_filter:
        placed_siswa_ids = PenempatanKelas.objects.filter(
            tahun_ajaran_id=ta_filter
        ).values_list('siswa_id', flat=True)
        queryset = queryset.exclude(id__in=placed_siswa_ids)

    # Filtering
    if search_query:
        queryset = queryset.filter(
            Q(nama_lengkap__icontains=search_query) | 
            Q(nisn__icontains=search_query)
        )
    if jk_filter:
        queryset = queryset.filter(jenis_kelamin=jk_filter)

    # Pagination
    paginator = Paginator(queryset, 10)
    page = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    # Logika pagination range
    current_page = page_obj.number
    total_pages = paginator.num_pages
    start_page = max(1, current_page - 2)
    end_page = min(total_pages, current_page + 2)
    page_range = range(start_page, end_page + 1)

    context = {
        'page_obj': page_obj,
        'page_range': page_range,
        'is_paginated': page_obj.has_other_pages(),
        'search_query': search_query,
        'jk_filter': jk_filter,
        'ta_filter': ta_filter,
        'list_ta': TahunAjaran.objects.all().order_by('-tahun'),
        'list_kelas': Kelas.objects.select_related('jurusan').order_by('tingkat', 'nama_kelas'),
    }
    
    return render(request, 'kesiswaan/penempatan_kelas_siswa_list.html', context)