# Sastreria
from django import forms
from .models import Perfil,Citas,Sastrerias,Renta,Venta
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # Registrar usuario
from django.shortcuts import get_object_or_404
import datetime

# Formulario de Registro
class SignupForm(UserCreationForm):
    # user = forms.CharField(max_length = 20, required = True, help_text = 'User name max lenght 30 characters.')
    #bio = formsself.CharField(max_length = 500,  )
    user_name = forms.CharField(max_length = 30, help_text = 'Enter first name, max 30 characters.')
    user_last = forms.CharField(max_length = 30, help_text = 'Enter last name, max 30 characters.')
    birth_date = forms.DateField(help_text = 'Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'user_name', 'user_last', 'birth_date', 'email' , 'password1', 'password2', )


# Editar Perfil
class EditProfileForm(UserChangeForm):
    birth_date = forms.DateField(help_text = 'Required. Format: YYYY-MM-DD')
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password')

class citas(forms.Form):
    citahora = forms.ChoiceField(choices=(("hora1",("08:00:00")),
                                        ("hora2",("09:00:00")),
                                        ("hora3",("10:00:00")),
                                        ("hora4",("11:00:00")),
                                        ("hora5",("12:00:00")),
                                        ("hora6",("13:00:00")),
                                        ("hora7",("14:00:00")),
                                        ("hora8",("15:00:00")),
                                        ("hora9",("16:00:00")),
                                        ("hora10",("17:00:00")),
                                        ("hora11",("18:00:00"))),label="Hora ",widget =forms.Select())
    citafecha = forms.DateField(widget=forms.SelectDateWidget(),initial=datetime.date.today)
    lugarcita = forms .ModelChoiceField(queryset=Sastrerias.objects.all())

class Ventaform(forms.Form):
    fecharecogida = forms.DateField(widget=forms.SelectDateWidget(),initial=datetime.date.today())
    tallanum = forms.ChoiceField(choices=(("talla1",("32")),
                                         ("talla2",("33")),
                                         ("talla3",("34")),
                                         ("talla4",("35")),
                                         ("talla5",("36")),
                                         ("talla6",("37")),
                                         ("talla7",("38")),
                                         ("talla8",("39")),
                                         ("talla9",("40")),
                                         ("talla10",("41")),
                                         ("talla11",("42")),
                                         ("talla12",("43")),
                                         ("talla13",("44")),
                                         ("talla14",("45")),
                                         ("talla15",("46")),
                                         ("talla16",("47")),
                                         ("talla17",("48")),
                                         ("talla18",("49")),
                                         ("talla19",("50"))),widget=forms.Select())
    tallamedida = forms.ChoiceField(choices=(("medida1",("Corto")),
                                            ("medida2",("Regular")),
                                            ("medida3",("Largo"))),widget=forms.Select())
    lugarrecogida = forms.ModelChoiceField(queryset=Sastrerias.objects.all())

class Rentaform(forms.Form):
    fecharecogida = forms.DateField(widget=forms.SelectDateWidget(),initial=datetime.date.today())
    finrenta = forms.DateField(widget=forms.SelectDateWidget(),initial=datetime.date.today())
    tallanum = forms.ChoiceField(choices=(("talla1",("32")),
                                         ("talla2",("33")),
                                         ("talla3",("34")),
                                         ("talla4",("35")),
                                         ("talla5",("36")),
                                         ("talla6",("37")),
                                         ("talla7",("38")),
                                         ("talla8",("39")),
                                         ("talla9",("40")),
                                         ("talla10",("41")),
                                         ("talla11",("42")),
                                         ("talla12",("43")),
                                         ("talla13",("44")),
                                         ("talla14",("45")),
                                         ("talla15",("46")),
                                         ("talla16",("47")),
                                         ("talla17",("48")),
                                         ("talla18",("49")),
                                         ("talla19",("50"))),widget=forms.Select())
    tallamedida = forms.ChoiceField(choices=(("medida1",("Corto")),
                                            ("medida2",("Regular")),
                                            ("medida3",("Largo"))),widget=forms.Select())
    lugarrecogida = forms.ModelChoiceField(queryset=Sastrerias.objects.all())