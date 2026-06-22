from django import forms
from .models import Siswa, DataOrangTua, DokumenSiswa

class SiswaForm(forms.ModelForm):
    class Meta:
        model = Siswa
        fields = ['nisn', 'nik', 'nama_lengkap', 'jenis_kelamin', 'tempat_lahir',
                  'tanggal_lahir', 'agama', 'golongan_darah', 'catatan_medis',
                  'alamat_tinggal', 'status_siswa', 'tanggal_masuk', 'tanggal_keluar',
                  'foto_masuk', 'foto_keluar']
        widgets = {
            'nisn': forms.TextInput(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'nik': forms.TextInput(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'nama_lengkap': forms.TextInput(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'tempat_lahir': forms.TextInput(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'tanggal_lahir': forms.DateInput(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300', 'type': 'date'}),
            'agama': forms.Select(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'golongan_darah': forms.Select(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'status_siswa': forms.Select(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'tanggal_masuk': forms.DateInput(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300', 'type': 'date'}),
            'tanggal_keluar': forms.DateInput(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300', 'type': 'date'}),
            'alamat_tinggal': forms.Textarea(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300', 'rows': 3}),
            'catatan_medis': forms.Textarea(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300', 'rows': 3}),
            'foto_masuk': forms.ClearableFileInput(attrs={'class': 'w-full text-sm'}),
            'foto_keluar': forms.ClearableFileInput(attrs={'class': 'w-full text-sm'}),
        }


class DataOrangTuaForm(forms.ModelForm):
    class Meta:
        model = DataOrangTua
        fields = ['nama_ayah', 'pekerjaan_ayah', 'no_hp_ayah',
                  'nama_ibu', 'pekerjaan_ibu', 'no_hp_ibu',
                  'nama_wali', 'pekerjaan_wali', 'no_hp_wali']
        widgets = {
            'nama_ayah': forms.TextInput(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'pekerjaan_ayah': forms.TextInput(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'no_hp_ayah': forms.TextInput(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'nama_ibu': forms.TextInput(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'pekerjaan_ibu': forms.TextInput(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'no_hp_ibu': forms.TextInput(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'nama_wali': forms.TextInput(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'pekerjaan_wali': forms.TextInput(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'no_hp_wali': forms.TextInput(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
        }


class DokumenSiswaForm(forms.ModelForm):
    class Meta:
        model = DokumenSiswa
        fields = ['jenis_dokumen', 'nama_dokumen', 'file_dokumen', 'keterangan']
        widgets = {
            'jenis_dokumen': forms.Select(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'nama_dokumen': forms.TextInput(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300'}),
            'keterangan': forms.Textarea(attrs={'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-3 py-2.5 text-neutral-800 focus:outline-none focus:ring-2 focus:ring-neutral-300', 'rows': 2}),
            'file_dokumen': forms.ClearableFileInput(attrs={'class': 'w-full text-sm'}),
        }