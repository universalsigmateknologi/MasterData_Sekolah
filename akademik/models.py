from django.db import models

class TahunAjaran(models.Model):
    id = models.BigAutoField(primary_key=True)
    tahun = models.CharField(max_length=9, help_text="Contoh: 2025/2026")
    semester = models.CharField(max_length=10, choices=[('Ganjil', 'Ganjil'), ('Genap', 'Genap')])
    is_aktif = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tahun_ajaran'
        unique_together = ('tahun', 'semester')

    def __str__(self):
        return f"{self.tahun} - {self.semester}"

class Jurusan(models.Model):
    id = models.BigAutoField(primary_key=True)
    nama_jurusan = models.CharField(max_length=100)
    kode_jurusan = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'jurusan'

    def __str__(self):
        return f"{self.kode_jurusan} - {self.nama_jurusan}"

class Kelas(models.Model):
    id = models.BigAutoField(primary_key=True)
    jurusan = models.ForeignKey('Jurusan', on_delete=models.SET_NULL, null=True, blank=True)
    nama_kelas = models.CharField(max_length=50)
    tingkat = models.IntegerField(help_text="10, 11, atau 12")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'kelas'

    def __str__(self):
        return self.nama_kelas