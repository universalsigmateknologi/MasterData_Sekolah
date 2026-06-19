from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views import View
from django.forms import modelformset_factory
from .models import Siswa, DokumenSiswa
from .forms import DokumenSiswaForm

DokumenSiswaFormSet = modelformset_factory(
    DokumenSiswa, form=DokumenSiswaForm,
    extra=0, can_delete=True
)


class SiswaDetailView(LoginRequiredMixin, DetailView):
    model = Siswa
    template_name = 'siswa/siswa_detail.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'siswa'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = self.request.GET.get('tab', 'identitas')
        context['dokumen_list'] = self.object.dokumen.all()
        context['log_list'] = self.object.log_riwayat.all()
        context['dokumen_form'] = DokumenSiswaForm()
        return context


class DokumenSiswaCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        siswa = get_object_or_404(Siswa, pk=pk)
        form = DokumenSiswaForm(request.POST, request.FILES)
        if form.is_valid():
            dokumen = form.save(commit=False)
            dokumen.siswa = siswa
            dokumen.save()
            messages.success(request, 'Dokumen berhasil ditambahkan.')
        else:
            for error in form.errors.values():
                messages.error(request, error.as_text())
        return redirect('siswa:detail', pk=pk)


class DokumenSiswaUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk, dokumen_id):
        siswa = get_object_or_404(Siswa, pk=pk)
        dokumen = get_object_or_404(DokumenSiswa, pk=dokumen_id, siswa=siswa)
        form = DokumenSiswaForm(request.POST, request.FILES, instance=dokumen)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dokumen berhasil diperbarui.')
        else:
            for error in form.errors.values():
                messages.error(request, error.as_text())
        return redirect('siswa:detail', pk=pk)


class DokumenSiswaDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, dokumen_id):
        siswa = get_object_or_404(Siswa, pk=pk)
        dokumen = get_object_or_404(DokumenSiswa, pk=dokumen_id, siswa=siswa)
        dokumen.delete()
        messages.success(request, 'Dokumen berhasil dihapus.')
        return redirect('siswa:detail', pk=pk)