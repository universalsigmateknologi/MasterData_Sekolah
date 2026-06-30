from django.db import models
from django.core.exceptions import ValidationError

class Pengaturan(models.Model):
    nama_program = models.CharField(max_length=100, verbose_name="Nama Program")
    # PERBAIKAN: Menggunakan upload_to
    logo = models.ImageField(upload_to="lokasi_logo/", verbose_name="Logo Program", blank=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pengaturan"
        verbose_name_plural = "Pengaturan"

    def clean(self):
        if Pengaturan.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Anda hanya dapat membuat satu data Pengaturan.")

    def save(self, *args, **kwargs):
        self.full_clean() 
        super(Pengaturan, self).save(*args, **kwargs)

    def __str__(self):
        return self.nama_program