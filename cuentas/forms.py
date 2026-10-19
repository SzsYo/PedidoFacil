from django.contrib.auth.forms import AuthenticationForm

from config.utils import BootstrapFormMixin


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    error_messages = {
        "invalid_login": "Usuario o contraseña incorrectos. Verifica tus datos e inténtalo de nuevo.",
        "inactive": "Esta cuenta está inactiva.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"autofocus": True, "placeholder": "Usuario"})
        self.fields["password"].widget.attrs.update({"placeholder": "Contraseña"})
