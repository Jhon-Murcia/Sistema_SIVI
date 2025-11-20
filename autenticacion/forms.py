from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class RegistroForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        help_text="Debe contener al menos 8 caracteres, incluir letras y números."
    )
    confirmar_password = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput
    )
    grupo = forms.ChoiceField(
        choices=[('Cliente', 'Cliente'), ('Vendedor', 'Vendedor')],
        label='Tipo de usuario',
        widget=forms.Select()
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        validate_password(password)  # Usa validaciones de Django (longitud, complejidad, etc.)
        return password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe un usuario con este correo electrónico.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")

        if password and confirmar_password and password != confirmar_password:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Encripta la contraseña
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
