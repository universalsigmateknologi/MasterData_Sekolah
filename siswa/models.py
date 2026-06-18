from django.db import models
import os

def get_upload_path(instance, filename):
    # Folder terpisah berdasarkan NISN
    return os.path.join('foto_siswa', instance.nisn if instance.nisn else 'temp', filename)

class Siswa(models.Model):
    STATUS_CHOICES = [
        ('Aktif', 'Aktif'),
        ('Lulus', 'Lulus'),
        ('Mutasi Keluar', 'Mutasi Keluar'),
        ('Drop Out', 'Drop Out'),
    ]
    
    JENIS_KELAMIN_CHOICES = [('L', 'Laki-laki'), ('P', 'Perempuan')]

    id = models.BigAutoField(primary_key=True)
    nisn = models.CharField(max_length=10, unique=True, null=True, blank=True)
    nik = models.CharField(max_length=16, unique=True, null=True, blank=True)
    nama_lengkap = models.CharField(max_length=255)
    jenis_kelamin = models.CharField(max_length=10, choices=JENIS_KELAMIN_CHOICES)
    tempat_lahir = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    agama = models.CharField(max_length=30, blank=True)
    golongan_darah = models.CharField(max_length=3, blank=True)
    catatan_medis = models.TextField(blank=True)
    alamat_tinggal = models.TextField()
    
    # Pelacakan Status
    status_siswa = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Aktif')
    tanggal_masuk = models.DateField(help_text="Tanggal resmi diterima")
    tanggal_keluar = models.DateField(null=True, blank=True)
    
    # Foto
    foto_masuk = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    foto_keluar = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'siswa'

    def __str__(self):
        return self.nama_lengkap

class DataOrangTua(models.Model):
    id = models.BigAutoField(primary_key=True)
    # OneToOne ke model Siswa di app yang sama
    siswa = models.OneToOneField(Siswa, on_delete=models.CASCADE, related_name='orang_tua')
    nama_ayah = models.CharField(max_length=255, blank=True)
    pekerjaan_ayah = models.CharField(max_length=100, blank=True)
    no_hp_ayah = models.CharField(max_length=20, blank=True)
    nama_ibu = models.CharField(max_length=255, blank=True)
    pekerjaan_ibu = models.CharField(max_length=100, blank=True)
    no_hp_ibu = models.CharField(max_length=20, blank=True)
    nama_wali = models.CharField(max_length=255, blank=True)
    pekerjaan_wali = models.CharField(max_length=100, blank=True)
    no_hp_wali = models.CharField(max_length=20, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'data_orang_tua'

    def __str__(self):
        return f"Orang Tua: {self.siswa.nama_lengkap}"