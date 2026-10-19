from django import forms


class BootstrapFormMixin:
    """Aplica clases de Bootstrap a los campos y marca los que tienen error."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            widget = campo.widget
            clase = "form-select" if isinstance(widget, forms.Select) else "form-control"
            widget.attrs["class"] = f"{widget.attrs.get('class', '')} {clase}".strip()

    def full_clean(self):
        super().full_clean()
        if self.is_bound and self._errors:
            for nombre in self._errors:
                if nombre in self.fields:
                    widget = self.fields[nombre].widget
                    widget.attrs["class"] = f"{widget.attrs.get('class', '')} is-invalid".strip()
