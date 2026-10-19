from django import forms

from config.utils import BootstrapFormMixin

from .models import Producto


class ProductoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio", "cantidad_disponible"]
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Ej: Teclado mecánico"}),
            "descripcion": forms.Textarea(attrs={"rows": 3, "data-max": 500}),
            "precio": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "cantidad_disponible": forms.NumberInput(attrs={"step": "1", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El límite lo controla JavaScript (data-max) para poder mostrar un mensaje claro
        self.fields["descripcion"].widget.attrs.pop("maxlength", None)

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre

    def clean_precio(self):
        precio = self.cleaned_data["precio"]
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")
        return precio

    def clean_cantidad_disponible(self):
        cantidad = self.cleaned_data["cantidad_disponible"]
        if cantidad < 0:
            raise forms.ValidationError("La cantidad disponible no puede ser negativa.")
        return cantidad
