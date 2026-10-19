from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CambiarEstadoForm, PedidoForm
from .models import Pedido


class PedidoLista(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = "pedidos/lista.html"
    context_object_name = "pedidos"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("usuario")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(cliente__icontains=q) | Q(numero_pedido__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "").strip()
        return ctx


class PedidoDetalle(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = "pedidos/detalle.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["estado_form"] = CambiarEstadoForm(initial={"estado": self.object.estado})
        return ctx


class PedidoCrear(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = "pedidos/form.html"
    success_url = reverse_lazy("pedidos:lista")
    success_message = "Pedido registrado correctamente."
    extra_context = {"titulo": "Nuevo pedido"}

    def form_valid(self, form):
        # El usuario autenticado queda asociado al pedido que registra
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class PedidoEditar(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = "pedidos/form.html"
    success_url = reverse_lazy("pedidos:lista")
    success_message = "Pedido actualizado correctamente."
    extra_context = {"titulo": "Editar pedido"}


class PedidoEliminar(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Pedido
    template_name = "pedidos/confirmar_eliminar.html"
    success_url = reverse_lazy("pedidos:lista")
    success_message = "Pedido eliminado correctamente."

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pedido = self.get_object()
            # "Eliminar cuando corresponda": un pedido confirmado no se elimina
            if pedido.estado == Pedido.Estado.CONFIRMADO:
                messages.error(
                    request,
                    "No se puede eliminar un pedido confirmado. Cámbialo a cancelado si ya no aplica.",
                )
                return redirect("pedidos:detalle", pk=pedido.pk)
        return super().dispatch(request, *args, **kwargs)


class PedidoCambiarEstado(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        form = CambiarEstadoForm(request.POST)
        if form.is_valid():
            pedido.estado = form.cleaned_data["estado"]
            pedido.save(update_fields=["estado"])
            messages.success(request, f"Estado actualizado a «{pedido.get_estado_display()}».")
        else:
            messages.error(request, "Selecciona un estado válido.")
        return redirect(reverse("pedidos:detalle", kwargs={"pk": pk}))
