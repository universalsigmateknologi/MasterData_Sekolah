from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Pilihan Status Pegawai (Untuk filtering)
STATUS_PEGAWAI_CHOICES = [
    ('PNS', 'PNS'),
    ('PPPK', 'PPPK'),
    ('GTY', 'Guru Tetap Yayasan'),
    ('PTY', 'Pegawai Tetap Yayasan'),
    ('Honorer', 'Honorer'),
    ('Magang', 'Magang'),
]

# Pilihan Jabatan Fungsional
JABATAN_CHOICES = [
    ('Kepala Sekolah', 'Kepala Sekolah'),
    ('Wakasek Kurikulum', 'Wakasek Kurikulum'),
    ('Wakasek Kesiswaan', 'Wakasek Kesiswaan'),
    ('Wakasek Sarana', 'Wakasek Sarana'),
    ('Guru Mapel', 'Guru Mata Pelajaran'),
    ('Wali Kelas', 'Wali Kelas'),
    ('Staff Tata Usaha', 'Staff Tata Usaha'),
    ('Staff Keuangan', 'Staff Keuangan'),
    ('IT Support', 'IT Support'),
]

class ProfileUser(models.Model):
    """
    Model ini menambahkan data tambahan ke User Django standar.
    Satu User memiliki satu ProfileUser.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Data Identitas Pegawai
    nip = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name="NIP / Nomor Induk")
    nuptk = models.CharField(max_length=16, blank=True, null=True, unique=True, verbose_name="NUPTK")
    
    # Data Pribadi
    jenis_kelamin = models.CharField(max_length=1, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], blank=True)
    tempat_lahir = models.CharField(max_length=50, blank=True)
    tanggal_lahir = models.DateField(blank=True, null=True)
    agama = models.CharField(max_length=20, blank=True)
    alamat = models.TextField(blank=True)
    no_telepon = models.CharField(max_length=20, blank=True, verbose_name="Nomor Telepon / WA")
    foto_profil = models.ImageField(upload_to='profiles/staff/', blank=True, null=True)

    # Data Kepegawaian
    jabatan = models.CharField(max_length=50, choices=JABATAN_CHOICES, default='Guru Mapel')
    status_pegawai = models.CharField(max_length=20, choices=STATUS_PEGAWAI_CHOICES, default='Honorer')
    tanggal_masuk = models.DateField(default=timezone.now)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.jabatan}"

    class Meta:
        verbose_name = "Profil Pegawai"
        verbose_name_plural = "Profil Pegawai"