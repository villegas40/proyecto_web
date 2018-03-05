from django.shortcuts import render
from .forms import SignupForm # Formulario creado para el perfil
from .models import Perfil
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate # singup up

# Create your views here.
def home(request):
    return render(request, 'pagina/home.html')

# Creacion de la vista de signup_view
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db() # Carga la instancia de perfil crada por signal
            user.perfil.fecha_nacimiento = form.cleaned_data.get('fecha_nacimiento')
            user.perfil.user_nombre = form.cleaned_data.get('user_nombre')
            user.perfil.user_apellido = form.cleaned_data.get('user_nombre')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = user.username, password = raw_password)
            login(request, user)
            return redirect('/perfil/') # Crear vista para perfil de usuario
    else:
        form = SignupForm()
    return render(request, 'pagina/signup.html', {'form': form})
