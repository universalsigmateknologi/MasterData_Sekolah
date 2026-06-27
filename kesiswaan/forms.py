from django import forms
from .models import MutasiSiswa
from siswa.models import Siswa

class MutasiSiswaForm(forms.ModelForm):
    class Meta:
        model = MutasiSiswa
        fields = [
            'siswa', 'jenis_mutasi', 'tanggal_mutasi', 
            'no_surat_mutasi', 'sekolah_asal_tujuan', 
            'alasan_mutasi', 'file_surat_mutasi'
        ]
        widgets = {
            'siswa': forms.Select(attrs={
                'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-4 py-2.5 outline-none focus:ring-2 focus:ring-neutral-300 focus:bg-white transition-all cursor-pointer',
                'placeholder': 'Cari dan pilih siswa...'
            }),
            'jenis_mutasi': forms.Select(attrs={
                'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-4 py-2.5 outline-none focus:ring-2 focus:ring-neutral-300 focus:bg-white transition-all cursor-pointer'
            }),
            'tanggal_mutasi': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-4 py-2.5 outline-none focus:ring-2 focus:ring-neutral-300 focus:bg-white transition-all cursor-pointer'
            }),
            'no_surat_mutasi': forms.TextInput(attrs={
                'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-4 py-2.5 outline-none focus:ring-2 focus:ring-neutral-300 focus:bg-white transition-all',
                'placeholder': 'Contoh: 001/SMK/X/2025'
            }),
            'sekolah_asal_tujuan': forms.TextInput(attrs={
                'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-4 py-2.5 outline-none focus:ring-2 focus:ring-neutral-300 focus:bg-white transition-all',
                'placeholder': 'Nama sekolah asal (jika masuk) atau sekolah tujuan (jika keluar)'
            }),
            'alasan_mutasi': forms.Textarea(attrs={
                'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-4 py-2.5 outline-none focus:ring-2 focus:ring-neutral-300 focus:bg-white transition-all resize-none',
                'rows': 4,
                'placeholder': 'Jelaskan alasan mutasi...'
            }),
            'file_surat_mutasi': forms.FileInput(attrs={
                'class': 'w-full text-sm text-neutral-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-medium file:bg-neutral-100 file:text-neutral-700 hover:file:bg-neutral-200 file:cursor-pointer file:transition-colors cursor-pointer'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hanya menampilkan siswa dengan status Aktif di dropdown
        self.fields['siswa'].queryset = Siswa.objects.filter(status_siswa='Aktif').order_by('nama_lengkap')
        self.fields['siswa'].empty_label = "Pilih Siswa Aktif..."
        
        # Set hari ini sebagai default value untuk tanggal mutasi
        if not self.initial.get('tanggal_mutasi'):
            from datetime import date
            self.initial['tanggal_mutasi'] = date.today()