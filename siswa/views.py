from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Siswa, DataOrangTua
from .forms import SiswaForm, DataOrangTuaForm

DataOrangTuaFormSet = inlineformset_factory(
    Siswa, DataOrangTua, form=DataOrangTuaForm,
    extra=1, can_delete=False, can_delete_extra=False
)

class SiswaListView(LoginRequiredMixin, ListView):
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

        paginator = context['paginator']
        current_page = context['page_obj'].number
        page_range = []
        for num in paginator.page_range:
            if num <= 3 or num > paginator.num_pages - 3:
                page_range.append(num)
            elif abs(num - current_page) <= 2:
                page_range.append(num)
        context['page_range'] = page_range

        return context


class SiswaCreateView(LoginRequiredMixin, CreateView):
    model = Siswa
    template_name = 'siswa/siswa_form.html'
    form_class = SiswaForm
    success_url = reverse_lazy('siswa:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ortu_form'] = DataOrangTuaFormSet(self.request.POST, self.request.FILES)
        else:
            context['ortu_form'] = DataOrangTuaFormSet()
        return context

    def form_valid(self, form):
        self.object = form.save()
        formset = DataOrangTuaFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if formset.is_valid():
            formset.save()
            messages.success(self.request, 'Data siswa berhasil ditambahkan.')
            return redirect(self.success_url)
        return self.form_invalid(form)


class SiswaUpdateView(LoginRequiredMixin, UpdateView):
    model = Siswa
    template_name = 'siswa/siswa_form.html'
    pk_url_kwarg = 'pk'
    form_class = SiswaForm
    success_url = reverse_lazy('siswa:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ortu_form'] = DataOrangTuaFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['ortu_form'] = DataOrangTuaFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ortu_form = context['ortu_form']
        self.object = form.save()
        if ortu_form.is_valid():
            ortu_form.save()
            messages.success(self.request, 'Data siswa berhasil diperbarui.')
            return redirect('siswa:index')
        return self.form_invalid(form)


class SiswaDeleteView(LoginRequiredMixin, DeleteView):
    model = Siswa
    template_name = 'siswa/siswa_confirm_delete.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('siswa:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Data siswa berhasil dihapus.')
        return response