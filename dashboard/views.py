from django.shortcuts import render
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from siswa.models import Siswa
from akademik.models import Kelas, Jurusan, TahunAjaran
from kesiswaan.models import PenempatanKelas


@login_required
def dashboard_admin(request):
    # 1. Statistik Umum Siswa
    total_siswa = Siswa.objects.count()
    siswa_aktif = Siswa.objects.filter(status_siswa='Aktif').count()
    siswa_lulus = Siswa.objects.filter(status_siswa='Lulus').count()
    siswa_mutasi = Siswa.objects.filter(status_siswa='Mutasi Keluar').count()
    siswa_do = Siswa.objects.filter(status_siswa='Drop Out').count()

    # 2. Statistik Akademik
    total_kelas = Kelas.objects.count()
    total_jurusan = Jurusan.objects.count()
    active_ta = TahunAjaran.objects.filter(is_aktif=True).first()

    # 3. Statistik Penempatan Kelas (Berdasarkan TA Aktif)
    siswa_sudah_penempatan = 0
    siswa_belum_penempatan = 0
    persen_penempatan = 0

    if active_ta:
        # Total siswa aktif yang seharusnya ditempatkan
        siswa_aktif_count = siswa_aktif
        
        # Hitung siswa yang sudah memiliki penempatan di TA aktif
        siswa_sudah_penempatan = PenempatanKelas.objects.filter(
            tahun_ajaran=active_ta
        ).values('siswa_id').distinct().count()
        
        siswa_belum_penempatan = siswa_aktif_count - siswa_sudah_penempatan
        
        if siswa_aktif_count > 0:
            persen_penempatan = round((siswa_sudah_penempatan / siswa_aktif_count) * 100)

    # 4. Distribusi Jenis Kelamin (Hanya Siswa Aktif)
    gender_stats = Siswa.objects.filter(status_siswa='Aktif').values('jenis_kelamin').annotate(count=Count('id'))
    laki_laki = next((item['count'] for item in gender_stats if item['jenis_kelamin'] == 'L'), 0)
    perempuan = next((item['count'] for item in gender_stats if item['jenis_kelamin'] == 'P'), 0)

    # 5. Distribusi Agama (Hanya Siswa Aktif)
    agama_stats = Siswa.objects.filter(status_siswa='Aktif').values('agama').annotate(count=Count('id')).order_by('-count')

    # 6. Siswa Terbaru (5 Terakhir)
    siswa_terbaru = Siswa.objects.order_by('-created_at')[:5]

    context = {
        # Umum
        'total_siswa': total_siswa,
        'siswa_aktif': siswa_aktif,
        'siswa_lulus': siswa_lulus,
        'siswa_mutasi': siswa_mutasi,
        'siswa_do': siswa_do,
        # Akademik
        'total_kelas': total_kelas,
        'total_jurusan': total_jurusan,
        'active_ta': active_ta,
        # Penempatan
        'siswa_sudah_penempatan': siswa_sudah_penempatan,
        'siswa_belum_penempatan': siswa_belum_penempatan,
        'persen_penempatan': persen_penempatan,
        # Demografi
        'laki_laki': laki_laki,
        'perempuan': perempuan,
        'agama_stats': agama_stats,
        # Latest
        'siswa_terbaru': siswa_terbaru,
    }

    return render(request, 'dashboard/dashboard_admin.html', context)