from django import forms
from .models import Pengaturan

class PengaturanForm(forms.ModelForm):
    class Meta:
        model = Pengaturan
        fields = ['nama_program', 'logo']
        widgets = {
            'nama_program': forms.TextInput(attrs={
                'class': 'w-full text-sm bg-neutral-50 border border-border-light rounded-xl px-4 py-2.5 outline-none focus:ring-2 focus:ring-neutral-300 focus:bg-white transition-all',
                'placeholder': 'Masukkan nama program / aplikasi'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'w-full text-sm text-neutral-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-medium file:bg-neutral-100 file:text-neutral-700 hover:file:bg-neutral-200 file:cursor-pointer file:transition-colors cursor-pointer',
                'accept': 'image/png, image/jpeg, image/webp'
            })
        }