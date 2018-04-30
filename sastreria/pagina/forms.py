# Sastreria
from django import forms
from .models import Perfil,Citas,Sastrerias
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # Registrar usuario
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
