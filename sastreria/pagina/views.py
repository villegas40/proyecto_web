# Sastreria
from django.shortcuts import render, redirect,get_object_or_404
from .forms import SignupForm, EditProfileForm,citas # Formulario creado para el perfil
from django.views.generic import UpdateView, FormView
from .models import Perfil, Product, Citas, Purchase, Orders
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate # singup up
from django.contrib.auth.forms import PasswordChangeForm # Formulario para cambiar contraseña
from django.contrib.auth import update_session_auth_hash # Mantener al usuario en sesion despues de cambiar contraseña
from django.contrib.auth.decorators import login_required # Decorador para que se necesite loguear para accesar ciertas vistas
from carton.cart import Cart # Importa de la aplicacion de carton_tags
from django.http import HttpResponseRedirect, HttpResponse
from sastreria.settings import BASE_URL
from django.conf import settings
from decimal import Decimal

# Create your views here.
def home(request):
    return render(request, 'pagina/index2.html')

def catalogo(request):
    if 'categoria' in request.GET:
        categoria = request.GET['categoria']
    else:
        categoria = 'todo'

    if 'filtrado' in request.GET:
        filtrado = request.GET['filtrado']
    else:
        filtrado = 'mostrar'

    if categoria == 'todo':
        item_list = Product.objects.all()
    else:
        item_list = Product.objects.filter(categoria=categoria)

    item_list = [item for item in item_list]

    if filtrado=='nuevo':
        item_list.sort(key=(lambda item: item.fecha_alta))
    elif filtrado=='barato':
        item_list.sort(key=(lambda item: item.precio), reverse=False)
    elif filtrado=='caro':
        item_list.sort(key=(lambda item: item.precio), reverse=True)
    elif filtrado=='mostrar':
        item_list.sort(key=(lambda item: item.nombre_producto))

    product = Product.objects.all()
    context = {
    'BASE_URL': BASE_URL,
    'categoria':categoria,
    'filtrado':filtrado,
    'item_list':item_list,
    'product':product,
    }
    return render(request, 'pagina/catalogo.html', context)
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
def info(request):
    product = Product.objects.get(id=request.GET.get('id'))
    return render(request, 'pagina/articulos.html', {'product': product})

@login_required
def show(request):

    return render(request, 'pagina/mostrar-carrito.html',{'paypal_url':settings.PAYPAL_URL,'paypal_email':settings.PAYPAL_EMAIL,'paypal_return_url':settings.PAYPAL_RETURN_URL})

@login_required
def remove(request):
    cart = Cart(request.session)
    product = Product.objects.get(id=request.GET.get('id'))
    cart.remove(product)
    #return HttpResponse("Removed")
    return render(request, 'pagina/eliminar-carrito.html', {'product':product})

def pagoCompletado(request,pk=None):
    cart = Cart(request.session)
    #dec = Decimal(pricet)
    dec = Decimal(cart.total) #Se hace asi , no cart.total()
    #print(dec1)
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    #orders = Orders()
    print("HOLAA")
        #for xd in Product:
        #product2 = Product.objects.all()
    #    prdct = Product.objects.filter(id = item.product.id)
    #    print(prdct)
        #print(type(product))

    #    if prdct.count() > 0:
            #print(Product.objects.filter(id = item.product.id).count())
        #    print(item.product.id)

    #        orders.nombre_producto.add(prdct)
    orders = Orders.objects.create(precioTotal=dec,purchaser=user,tx="1",status="NOPAGADO")
    for item in cart.items:
        orders.nombre_producto.add(Product.objects.get(id=item.product.id))
        '''
    orders.precioTotal = dec
    orders.purchaser = user
    orders.tx = "test"
    orders.status = "SINPAGAR"
    for item in cart.items:
        print ("HOLA QUE TAL SOY UN PRINT")
        orders.nombre_producto.add(Product.objects.get(id=item.product.id))
    #orders.save()
    '''

    print(orders.id)
    rorders = get_object_or_404(Orders,pk=orders.id)
    return render(request, 'pagina/pago.html',{'resource':Cart(request.session),'orden':rorders,'paypal_url':settings.PAYPAL_URL,'paypal_email':settings.PAYPAL_EMAIL,'paypal_return_url':settings.PAYPAL_RETURN_URL})

def eliminarCarrito(request):
    cart = Cart(request.session)
    cart.clear()
    return HttpResponse("Carrito Vacio")

'''Checar despues
@login_required
def removeSingle(request):
    cart = Cart(request.session)
    product = Product.objects.get(id=request.GET.get('id'))
    cart.remove_single(product)
    return redirect(request, 'pagina/mostrar-carrito.html', {'product':product})
 Usar este metodo para que cuando le de al boton de pagar despliegue el contenido
 del pedido y asi poder proceder a pagar , cuando este pague cambiara el payment_status
 del modelo a pagado y asi poder desplegar todo.
 si no se realiza el pago el payment_status continuara en sin pagar
 Tareas a investigar:
 -Como modifcar un modelo,registro
 -mandar el registro a la siguiente template
 -como guardar un ManyToManyField viniendo del Carrito
'''
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
            #poner aqui una alerta chida
            return HttpResponseRedirect("/home/")
    else:
        form = citas()
    ctx = {"form":form}

    return render(request,'pagina/citas.html',ctx)
@login_required
def desplegarcitas(request,pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user

    p = Citas.objects.all().filter(usuario = user)

    return render(request,'pagina/desplegarcitas.html',{'list': Citas.objects.all().filter(usuario=user)})
@login_required
def mostrarpedidos(request,pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user =request.user

    return render(request,'pagina/mostrarpedidos.html',{'list':Orders.objects.all().filter(purchaser=user,status="PAGADO")})


@login_required
def citasdescripcion(request,id):
    resource = get_object_or_404(Citas,pk=id)
    return render(request,'pagina/descripcioncitas.html',{'resource':resource})

@login_required
def pedidosdescripcion(request,id):
    resource = get_object_or_404(Orders,pk=id)
    return render(request,'pagina/pedidosdescripcion.html',{'resource':resource})


def sucursalesv(request):
    return render(request,'pagina/sastrerias.html')
