from django.db import models
import os

def get_surat_path(instance, filename):
    return os.path.join('surat_mutasi', filename)

def get_berkas_path(instance, filename):
    # Path berdasarkan nama berkas
    return os.path.join('berkas_siswa', instance.nama_berkas, filename)

class PenempatanKelas(models.Model):
    KETERANGAN_CHOICES = [
        ('Aktif', 'Aktif'),
        ('Naik Kelas', 'Naik Kelas'),
        ('Tinggal Kelas', 'Tinggal Kelas'),
    ]

    id = models.BigAutoField(primary_key=True)
    # Referensi ke app siswa (String reference)
    siswa = models.ForeignKey('siswa.Siswa', on_delete=models.CASCADE, related_name='riwayat_kelas')
    # Referensi ke app akademik (String reference)
    kelas = models.ForeignKey('akademik.Kelas', on_delete=models.CASCADE)
    tahun_ajaran = models.ForeignKey('akademik.TahunAjaran', on_delete=models.CASCADE)
    keterangan = models.CharField(max_length=20, choices=KETERANGAN_CHOICES, default='Aktif')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'penempatan_kelas'
        unique_together = ('siswa', 'tahun_ajaran')

    def __str__(self):
        return f"{self.siswa.nama_lengkap} - {self.kelas.nama_kelas}"

class MutasiSiswa(models.Model):
    JENIS_MUTASI_CHOICES = [('Masuk', 'Masuk'), ('Keluar', 'Keluar')]

    id = models.BigAutoField(primary_key=True)
    siswa = models.ForeignKey('siswa.Siswa', on_delete=models.CASCADE, related_name='mutasi')
    jenis_mutasi = models.CharField(max_length=10, choices=JENIS_MUTASI_CHOICES)
    tanggal_mutasi = models.DateField()
    alasan_mutasi = models.TextField()
    sekolah_asal_tujuan = models.CharField(max_length=255)
    no_surat_mutasi = models.CharField(max_length=100)
    file_surat_mutasi = models.FileField(upload_to=get_surat_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mutasi_siswa'

    def __str__(self):
        return f"{self.jenis_mutasi} - {self.siswa.nama_lengkap}"

class BerkasSiswa(models.Model):
    id = models.BigAutoField(primary_key=True)
    siswa = models.ForeignKey('siswa.Siswa', on_delete=models.CASCADE, related_name='berkas')
    nama_berkas = models.CharField(max_length=50) # Contoh: KK, Ijazah
    file_path = models.FileField(upload_to=get_berkas_path)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'berkas_siswa'

    def __str__(self):
        return f"{self.nama_berkas} - {self.siswa.nama_lengkap}"