from django import forms
from .models import TahunAjaran


class TahunAjaranForm(forms.ModelForm):
    class Meta:
        model = TahunAjaran
        fields = ['tahun', 'semester', 'is_aktif']
        widgets = {
            'tahun': forms.TextInput(attrs={
                'class': 'w-full text-sm border border-neutral-200 rounded-xl px-3 py-2.5 outline-none focus:ring-2 focus:ring-neutral-300 focus:border-transparent transition-all',
                'placeholder': 'Contoh: 2025/2026',
            }),
            'semester': forms.Select(attrs={
                'class': 'w-full text-sm border border-neutral-200 rounded-xl px-3 py-2.5 outline-none focus:ring-2 focus:ring-neutral-300 focus:border-transparent transition-all bg-white',
            }),
            'is_aktif': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 rounded border-neutral-300 text-neutral-900 focus:ring-neutral-300 cursor-pointer',
            }),
        }
        labels = {
            'tahun': 'Tahun Ajaran',
            'semester': 'Semester',
            'is_aktif': 'Jadikan Tahun Ajaran Aktif',
        }
        error_messages = {
            'tahun': {
                'required': 'Tahun ajaran wajib diisi.',
                'max_length': 'Tahun ajaran maksimal 9 karakter.',
            },
            'semester': {
                'required': 'Semester wajib dipilih.',
            },
        }
