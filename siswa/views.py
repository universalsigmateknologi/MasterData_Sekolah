from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Siswa

class SiswaListView(ListView):
    model = Siswa
    template_name = 'siswa/siswa_list.html'
    context_object_name = 'siswa_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')
        jenis_kelamin = self.request.GET.get('jenis_kelamin')

        if search:
            queryset = queryset.filter(
                Q(nama_lengkap__icontains=search) |
                Q(nisn__icontains=search) |
                Q(nik__icontains=search)
            )
        if status:
            queryset = queryset.filter(status_siswa=status)
        if jenis_kelamin:
            queryset = queryset.filter(jenis_kelamin=jenis_kelamin)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['jk_filter'] = self.request.GET.get('jenis_kelamin', '')

        # Generate page range for pagination
        paginator = context['paginator']
        page_numbers = paginator.page_range
        current_page = context['page_obj'].number
        # Show current page and 2 pages before/after, plus first and last pages
        page_range = []
        for num in page_numbers:
            if num <= 3 or num > paginator.num_pages - 3:
                page_range.append(num)
            elif abs(num - current_page) <= 2:
                page_range.append(num)
        context['page_range'] = page_range

        return context


class SiswaCreateView(CreateView):
    model = Siswa
    template_name = 'siswa/siswa_form.html'
    fields = ['nisn', 'nik', 'nama_lengkap', 'jenis_kelamin', 'tempat_lahir',
              'tanggal_lahir', 'agama', 'golongan_darah', 'catatan_medis',
              'alamat_tinggal', 'status_siswa', 'tanggal_masuk', 'tanggal_keluar',
              'foto_masuk', 'foto_keluar']
    success_url = reverse_lazy('siswa:index')
    success_message = 'Data siswa berhasil ditambahkan.'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Data siswa berhasil ditambahkan.')
        return response


class SiswaUpdateView(UpdateView):
    model = Siswa
    template_name = 'siswa/siswa_form.html'
    pk_url_kwarg = 'pk'
    fields = ['nisn', 'nik', 'nama_lengkap', 'jenis_kelamin', 'tempat_lahir',
              'tanggal_lahir', 'agama', 'golongan_darah', 'catatan_medis',
              'alamat_tinggal', 'status_siswa', 'tanggal_masuk', 'tanggal_keluar',
              'foto_masuk', 'foto_keluar']
    success_url = reverse_lazy('siswa:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Data siswa berhasil diperbarui.')
        return response


class SiswaDeleteView(DeleteView):
    model = Siswa
    template_name = 'siswa/siswa_confirm_delete.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('siswa:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Data siswa berhasil dihapus.')
        return response