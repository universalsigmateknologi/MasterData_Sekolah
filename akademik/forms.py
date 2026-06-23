from django import forms
from .models import TahunAjaran, Jurusan, Kelas


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


class JurusanForm(forms.ModelForm):
    class Meta:
        model = Jurusan
        fields = ['kode_jurusan', 'nama_jurusan']
        widgets = {
            'kode_jurusan': forms.TextInput(attrs={
                'class': 'w-full text-sm border border-neutral-200 rounded-xl px-3 py-2.5 outline-none focus:ring-2 focus:ring-neutral-300 focus:border-transparent transition-all',
                'placeholder': 'Contoh: TKJ, RPL, AK',
            }),
            'nama_jurusan': forms.TextInput(attrs={
                'class': 'w-full text-sm border border-neutral-200 rounded-xl px-3 py-2.5 outline-none focus:ring-2 focus:ring-neutral-300 focus:border-transparent transition-all',
                'placeholder': 'Contoh: Teknik Komputer Jaringan',
            }),
        }
        labels = {
            'kode_jurusan': 'Kode Jurusan',
            'nama_jurusan': 'Nama Jurusan',
        }


class KelasForm(forms.ModelForm):
    class Meta:
        model = Kelas
        fields = ['nama_kelas', 'tingkat', 'jurusan']
        widgets = {
            'nama_kelas': forms.TextInput(attrs={
                'class': 'w-full text-sm border border-neutral-200 rounded-xl px-3 py-2.5 outline-none focus:ring-2 focus:ring-neutral-300 focus:border-transparent transition-all',
                'placeholder': 'Contoh: X TKJ 1',
            }),
            'tingkat': forms.Select(
                choices=[(10, 'Kelas 10'), (11, 'Kelas 11'), (12, 'Kelas 12')],
                attrs={
                    'class': 'w-full text-sm border border-neutral-200 rounded-xl px-3 py-2.5 outline-none focus:ring-2 focus:ring-neutral-300 focus:border-transparent transition-all bg-white',
                }
            ),
            'jurusan': forms.Select(attrs={
                'class': 'w-full text-sm border border-neutral-200 rounded-xl px-3 py-2.5 outline-none focus:ring-2 focus:ring-neutral-300 focus:border-transparent transition-all bg-white',
            }),
        }
        labels = {
            'nama_kelas': 'Nama Kelas',
            'tingkat': 'Tingkat',
            'jurusan': 'Jurusan',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['jurusan'].queryset = Jurusan.objects.all().order_by('kode_jurusan')
        self.fields['jurusan'].empty_label = '-- Pilih Jurusan (opsional) --'
