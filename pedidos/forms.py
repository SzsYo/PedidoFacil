from django import forms

from config.utils import BootstrapFormMixin

from .models import Pedido


class PedidoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["numero_pedido", "cliente", "descripcion", "valor_total", "estado"]
        widgets = {
            "numero_pedido": forms.TextInput(attrs={"placeholder": "Ej: PED-0001"}),
            "cliente": forms.TextInput(attrs={"placeholder": "Nombre del cliente"}),
            "descripcion": forms.Textarea(attrs={"rows": 3, "data-max": 500}),
            "valor_total": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }
        error_messages = {
            "numero_pedido": {"unique": "Ya existe un pedido con este número. Usa uno diferente."},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["descripcion"].widget.attrs.pop("maxlength", None)

    def clean_numero_pedido(self):
        return self.cleaned_data["numero_pedido"].strip()

    def clean_valor_total(self):
        valor = self.cleaned_data["valor_total"]
        if valor <= 0:
            raise forms.ValidationError("El valor total debe ser mayor que cero.")
        return valor


class CambiarEstadoForm(forms.Form):
    estado = forms.ChoiceField(
        choices=Pedido.Estado.choices,
        error_messages={"invalid_choice": "Selecciona un estado válido."},
    )
