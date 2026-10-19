from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ProductoForm
from .models import Producto


class ProductoLista(LoginRequiredMixin, ListView):
    model = Producto
    template_name = "productos/lista.html"
    context_object_name = "productos"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(nombre__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "").strip()
        return ctx


class ProductoDetalle(LoginRequiredMixin, DetailView):
    model = Producto
    template_name = "productos/detalle.html"


class ProductoCrear(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/form.html"
    success_url = reverse_lazy("productos:lista")
    success_message = "Producto creado correctamente."
    extra_context = {"titulo": "Nuevo producto"}


class ProductoEditar(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/form.html"
    success_url = reverse_lazy("productos:lista")
    success_message = "Producto actualizado correctamente."
    extra_context = {"titulo": "Editar producto"}


class ProductoEliminar(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Producto
    template_name = "productos/confirmar_eliminar.html"
    success_url = reverse_lazy("productos:lista")
    success_message = "Producto eliminado correctamente."
