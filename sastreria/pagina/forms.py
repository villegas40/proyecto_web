from django import forms
from .models import Perfil
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm # Registrar usuario

# Formulario de Registro
class SignupForm(UserCreationForm):
    user_nombre = forms.CharField(max_length = 30, help_text = 'Enter first name, max 30 characters.')
    user_apellido = forms.CharField(max_length = 30, help_text = 'Enter last name, max 30 characters.')
    fecha_nacimiento = forms.DateField(help_text = 'Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'user_nombre', 'user_apellido', 'fecha_nacimiento',
        'password1', 'password2')
