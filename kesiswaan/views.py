from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import PenempatanKelas, MutasiSiswa
from akademik.models import Kelas, TahunAjaran
from siswa.models import Siswa
from .forms import MutasiSiswaForm
from django.contrib import messages

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

@login_required
def mutasi_siswa_list(request):
    # Mengambil parameter GET untuk filter
    search_query = request.GET.get('search', '')
    jenis_filter = request.GET.get('jenis_mutasi', '')

    # Base queryset dengan select_related untuk optimasi db query
    queryset = MutasiSiswa.objects.select_related('siswa').order_by('-tanggal_mutasi', '-created_at')

    # Logika filtering
    if search_query:
        queryset = queryset.filter(
            Q(siswa__nama_lengkap__icontains=search_query) | 
            Q(siswa__nisn__icontains=search_query) |
            Q(no_surat_mutasi__icontains=search_query)
        )
    if jenis_filter:
        queryset = queryset.filter(jenis_mutasi=jenis_filter)

    # Pagination
    paginator = Paginator(queryset, 10) # 10 item per halaman
    page = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    # Logika untuk menampilkan rentang halaman dinamis di pagination
    current_page = page_obj.number
    total_pages = paginator.num_pages
    page_range = []
    for num in paginator.page_range:
        if num <= 3 or num > total_pages - 3:
            page_range.append(num)
        elif abs(num - current_page) <= 2:
            page_range.append(num)

    # Hitung ringkasan untuk kartu statistik
    total_mutasi_masuk = MutasiSiswa.objects.filter(jenis_mutasi='Masuk').count()
    total_mutasi_keluar = MutasiSiswa.objects.filter(jenis_mutasi='Keluar').count()

    context = {
        'page_obj': page_obj,
        'page_range': page_range,
        'is_paginated': page_obj.has_other_pages(),
        # Nilai filter saat ini
        'search_query': search_query,
        'jenis_filter': jenis_filter,
        # Statistik
        'total_mutasi_masuk': total_mutasi_masuk,
        'total_mutasi_keluar': total_mutasi_keluar,
    }
    
    return render(request, 'kesiswaan/mutasi_siswa_list.html', context)

def mutasi_create(request):
    if request.method == 'POST':
        form = MutasiSiswaForm(request.POST, request.FILES)
        if form.is_valid():
            mutasi = form.save()
            if mutasi.jenis_mutasi == 'Keluar':
                messages.success(request, f'Data mutasi siswa berhasil ditambahkan dan penempatan kelas {mutasi.siswa.nama_lengkap} telah dihapus.')
            else:
                messages.success(request, 'Data mutasi siswa berhasil ditambahkan.')
            return redirect('kesiswaan:mutasi_list')
    else:
        form = MutasiSiswaForm()

    # AMBIL DATA SISWA AKTIF UNTUK DROPDOWN CUSTOM
    list_siswa_aktif = Siswa.objects.filter(status_siswa='Aktif').order_by('nama_lengkap')

    context = {
        'form': form,
        'list_siswa_aktif': list_siswa_aktif, # Dikirim ke template
    }
    return render(request, 'kesiswaan/mutasi_form.html', context)


def kenaikan_kelas_view(request):
    # Mengambil parameter GET untuk setup awal
    ta_asal_id = request.GET.get('ta_asal', '')
    kelas_asal_id = request.GET.get('kelas_asal', '')
    ta_tujuan_id = request.GET.get('ta_tujuan', '')

    active_ta = TahunAjaran.objects.filter(is_aktif=True).first()
    
    # Default TA Asal adalah TA yang sedang aktif
    if not ta_asal_id and active_ta:
        ta_asal_id = str(active_ta.id)

    # ------------------- POST LOGIC (PROSES) -------------------
    if request.method == 'POST':
        selected_placement_ids = request.POST.getlist('selected_placements')
        action_type = request.POST.get('action_type')
        target_kelas_id = request.POST.get('target_kelas')
        target_ta_id = request.POST.get('ta_tujuan') # <-- SUDAH DIPERBAIKI

        if not selected_placement_ids:
            messages.error(request, 'Pilih minimal satu siswa untuk diproses.')
        else:
            try:
                # Ambil query object yang akan diupdate (bukan langsung di-evaluate)
                old_placements = PenempatanKelas.objects.filter(id__in=selected_placement_ids)

                if action_type == 'naik':
                    if not target_kelas_id or not target_ta_id:
                        messages.error(request, 'Pilih Kelas Tujuan dan Tahun Ajaran Tujuan.')
                    else:
                        # 1. Ubah status kelas lama
                        old_placements.update(keterangan='Naik Kelas')
                        
                        # 2. Buat data penempatan kelas baru
                        new_placements = [
                            PenempatanKelas(
                                siswa_id=p.siswa_id,
                                kelas_id=target_kelas_id,
                                tahun_ajaran_id=target_ta_id,
                                keterangan='Aktif'
                            ) for p in old_placements
                        ]
                        PenempatanKelas.objects.bulk_create(new_placements, ignore_conflicts=True)
                        
                        kelas_name = Kelas.objects.get(id=target_kelas_id).nama_kelas
                        messages.success(request, f'Berhasil menaikkan {len(new_placements)} siswa ke kelas {kelas_name}.')

                elif action_type == 'tinggal':
                    # Hanya mengubah status kelas lama
                    updated = old_placements.update(keterangan='Tinggal Kelas')
                    messages.success(request, f'Berhasil menandai {updated} siswa sebagai Tinggal Kelas.')

            except Exception as e:
                messages.error(request, f'Terjadi kesalahan sistem: {str(e)}')

            # Redirect agar halaman merefresh data terbaru tanpa resubmit form
            return redirect(request.get_full_path())

    # ------------------- GET LOGIC (DISPLAY) -------------------
    list_placements = []
    
    # Jika filter sudah lengkap, ambil data siswa yang ada di kelas asal tersebut
    if ta_asal_id and kelas_asal_id:
        list_placements = PenempatanKelas.objects.select_related(
            'siswa', 'kelas', 'tahun_ajaran'
        ).filter(
            tahun_ajaran_id=ta_asal_id,
            kelas_id=kelas_asal_id,
            keterangan='Aktif' # Hanya yang statusnya masih aktif di kelas tersebut
        ).order_by('siswa__nama_lengkap')

    context = {
        'ta_asal_id': ta_asal_id,
        'kelas_asal_id': kelas_asal_id,
        'ta_tujuan_id': ta_tujuan_id,
        'list_placements': list_placements,
        'list_ta': TahunAjaran.objects.all().order_by('-tahun'),
        'list_kelas': Kelas.objects.select_related('jurusan').order_by('tingkat', 'nama_kelas'),
    }
    
    return render(request, 'kesiswaan/kenaikan_kelas.html', context)

def kelulusan_massal_view(request):
    # Cari TA yang sedang aktif DAN semesternya Genap (karena kelulusan hanya di akhir genap)
    active_ta = TahunAjaran.objects.filter(is_aktif=True, semester='Genap').first()

    # ------------------- POST LOGIC (PROSES) -------------------
    if request.method == 'POST':
        selected_placement_ids = request.POST.getlist('selected_placements')
        tanggal_sk = request.POST.get('tanggal_sk')

        if not selected_placement_ids:
            messages.error(request, 'Pilih minimal satu siswa untuk diproses kelulusan.')
        elif not tanggal_sk:
            messages.error(request, 'Tanggal SK Kelulusan wajib diisi.')
        elif not active_ta:
            messages.error(request, 'Tidak dapat memproses. Tidak ada Tahun Ajaran Genap yang sedang aktif.')
        else:
            try:
                # Ambil data penempatan kelas kelas 12 yang dipilih
                placements = PenempatanKelas.objects.filter(id__in=selected_placement_ids)
                
                # 1. Ubah status penempatan kelas menjadi 'Lulus'
                placements.update(keterangan='Lulus')
                
                # 2. Ubah status siswa menjadi 'Lulus' dan isi tanggal_keluar
                siswa_ids = placements.values_list('siswa_id', flat=True)
                updated_siswa = Siswa.objects.filter(id__in=siswa_ids).update(
                    status_siswa='Lulus',
                    tanggal_keluar=tanggal_sk
                )
                
                messages.success(request, f'Berhasil memproses kelulusan {updated_siswa} siswa.')
            except Exception as e:
                messages.error(request, f'Terjadi kesalahan sistem: {str(e)}')

            return redirect(request.get_full_path())

    # ------------------- GET LOGIC (DISPLAY) -------------------
    list_placements = []
    
    # Jika ada TA aktif semester genap, langsung ambil data kelas 12
    if active_ta:
        list_placements = PenempatanKelas.objects.select_related(
            'siswa', 'kelas__jurusan', 'tahun_ajaran'
        ).filter(
            tahun_ajaran=active_ta,
            kelas__tingkat=12,
            keterangan='Aktif'
        ).order_by('kelas__nama_kelas', 'siswa__nama_lengkap')

    context = {
        'active_ta': active_ta, # Dikirim untuk pengecekan di template
        'list_placements': list_placements,
    }
    
    return render(request, 'kesiswaan/kelulusan_massal.html', context)


def cetak_buku_induk_view(request):
    ta_filter = request.GET.get('ta_filter', '')

    # Base queryset: Siswa yang sudah dinyatakan Lulus
    queryset = Siswa.objects.filter(status_siswa='Lulus').order_by('-tanggal_keluar', 'nama_lengkap')

    # Jika filter TA dipilih, hanya tampilkan siswa yang lulus di TA tersebut
    if ta_filter:
        lulus_siswa_ids = PenempatanKelas.objects.filter(
            tahun_ajaran_id=ta_filter,
            keterangan='Lulus'
        ).values_list('siswa_id', flat=True)
        queryset = queryset.filter(id__in=lulus_siswa_ids)

    context = {
        'ta_filter': ta_filter,
        'list_ta': TahunAjaran.objects.all().order_by('-tahun'),
        'siswa_list': queryset, # Ditampilkan semua (tanpa pagination karena untuk arsip)
    }
    
    return render(request, 'kesiswaan/cetak_buku_induk.html', context)