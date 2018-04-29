# Sastreria
from django.shortcuts import render, redirect,get_object_or_404
from .forms import SignupForm, EditProfileForm,citas,Ventaform,Rentaform # Formulario creado para el perfil
from django.views.generic import UpdateView, FormView
from .models import Perfil, Product,Citas,Renta,Venta
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate # singup up
from django.contrib.auth.forms import PasswordChangeForm # Formulario para cambiar contraseña
from django.contrib.auth import update_session_auth_hash # Mantener al usuario en sesion despues de cambiar contraseña
from django.contrib.auth.decorators import login_required # Decorador para que se necesite loguear para accesar ciertas vistas
from carton.cart import Cart,CartItem # Importa de la aplicacion de carton_tags
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def home(request):
    product = Product.objects.all()
    return render(request, 'pagina/index.html', {'product': product})

# Creacion de la vista de signup_view
def signup_user_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db() # Carga la instancia de perfil crada por signal
            user.perfil.birth_date = form.cleaned_data.get('birth_date')
            user.perfil.user_name = form.cleaned_data.get('user_name')
            user.perfil.user_last = form.cleaned_data.get('user_last')
            user.first_name = user.perfil.user_name
            user.last_name = user.perfil.user_last
            user.perfil.email = user.email
            user.save()
            # user.perfil.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = user.username, password = raw_password)
            login(request, user)
            return redirect('/profile/')

    else:
        form = SignupForm()
    return render(request, 'pagina/register.html', {'form': form})

@login_required
def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'pagina/profile.html', args)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            user = form.save()
            user.perfil.user_name = user.first_name
            user.perfil.user_last = user.last_name
            user.perfil.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            return redirect('/profile/')
    else:
        form = EditProfileForm(instance = request.user)
    return render(request, 'pagina/edit_profile.html', {'form': form})

# Vista cambiar contraseña
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST, user = request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile/')
        else:
            return redirect('/change_password/')
    else:
        form = PasswordChangeForm(user = request.user)
    return render(request, 'pagina/change_password.html', {'form': form})

# Agregar carrito de compras
@login_required
def add(request):
    cart = Cart(request.session)
    product = Product.objects.get(id=request.GET.get('id'))
    cart.add(product, price=product.precio, quantity=1)
    #return HttpResponse("Añadido al carrito.")
    return render(request, 'pagina/agregar-carrito.html', {'product': product})


@login_required
def show(request):
    
    return render(request, 'pagina/mostrar-carrito.html')

@login_required
def remove(request):
    cart = Cart(request.session)
    product = Product.objects.get(id=request.GET.get('id'))
    cart.remove(product)
    #return HttpResponse("Removed")
    return render(request, 'pagina/eliminar-carrito.html', {'product':product})

@login_required
def modulocitas(request,id):
    form = citas()
    if request.method == 'POST':
        form = citas(request.POST,request.FILES)
        if form.is_valid():
            user = get_object_or_404(User,pk=id)
            p = Citas()

            p.CitaHora = form.cleaned_data["citahora"]
            p.CitaFecha = form.cleaned_data["citafecha"]
            p.LugarCita = form.cleaned_data["lugarcita"]
            p.usuario = user
            p.save()
            return HttpResponseRedirect("/home/")
    else:
        form = citas()
    ctx = {"form":form}

    return render(request,'pagina/citas.html',ctx)

@login_required
def moduloventa(request,id):
    form = Ventaform()
    if request.method == 'POST':
        form = Ventaform(request.POST,request.FILES)
        if form.is_valid():
            tux = get_object_or_404(Product,pk=id)
            p = Venta()
            p.FechaDeRecogida = form.cleaned_data["fecharecogida"]
            p.TallaNum = form.cleaned_data["tallanum"]
            p.TallaMedida = form.cleaned_data["tallamedida"]
            p.LugarRecogida = form.cleaned_data["lugarrecogida"]
            p.Tuxedo = tux
            p.save()
            return HttpResponseRedirect("/carrito/agregar/?id="+id)
    else:
        form = Ventaform()

    ctx = {"form":form}
    return render(request,'pagina/ventatraje.html',ctx)

@login_required
def modulorenta(request,id):
    form = Rentaform()
    if request.method == 'POST':
        form = Rentaform(request.POST,request.FILES)
        if form.is_valid():
            tux = get_object_or_404(Product,pk=id)
            p = Renta()
            p.InicioRenta = form.cleaned_data['fecharecogida']
            p.FinRenta = form.cleaned_data['finrenta']
            p.TallaNum = form.cleaned_data['tallanum']
            p.TallaMedida = form.cleaned_data['tallamedida']
            p.Tuxedo = tux
            p.LugarRecogida = form.cleaned_data['lugarrecogida']
            p.save()
            return HttpResponseRedirect("/carrito/agregar/?id="+id)
    else:
        form = Rentaform()

    ctx = {"form":form}
    return render(request,'pagina/rentatraje.html',ctx)



