"""sastreria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views # Para usar login y logout
from pagina import views
from pagina.views import modulocitas,moduloventa,modulorenta
from pagos.views import descripcion,purchased,error,download,downloadr
# Importar las vistas genericas ofrecidas por django para resetear contraseña
from django.contrib.auth.views import (
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.login, {'template_name': 'pagina/login.html'}, name = 'login'),
    path('logout/', auth_views.logout, {'template_name':'pagina/logout.html'}, name='logout'),
    path('home/', views.home, name = 'home_view'),
    path('register/', views.signup_user_view, name = 'register_view'),
    path('profile/', views.view_profile, name = "profile_view"),
    path('edit_profile/', views.edit_profile, name = 'edit_profile_view'),
    path('change_password/', views.change_password, name = 'change_password_view'),
    re_path(r'^password_reset/$', password_reset, {'template_name':'reset/password_reset_form.html',
    'email_template_name':'reset/password_reset_email.html'}, name = 'password_reset'),
    re_path(r'^password_reset_done/$', password_reset_done, {'template_name': 'reset/password_reset_done.html'},
    name = 'password_reset_done'),
    re_path(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name':'reset/password_reset_confirm.html',},
    name = 'password_reset_confirm'),
    re_path(r'^password_reset_complete/$', password_reset_complete, {'template_name':'reset/password_reset_complete.html',},
    name = 'password_reset_complete'),
    path('carrito/mostrar/', views.show, name='mostrar_carrito_view'),
    re_path(r'^carrito/agregar/$',views.add, name='agregar_carrito_view'),
    re_path(r'^carrito/remover/$',views.remove, name='agregar_carrito_view'),
    #NUEVAS URL
    re_path(r'citas/(?P<id>\d+)/$',modulocitas,name='modulocitas'),
    path('error/',error,name='erro'),
    re_path(r'^download/(?P<id>\d+)/$',download),
    re_path(r'^downloadr/(?P<id>\d+)/$',downloadr),
    re_path(r'^purchased/(?P<uid>\d+)/(?P<id>\d+)/$',purchased),
    re_path(r'VentaTraje/(?P<id>\d+)/$',moduloventa,name='moduloventa'),
    re_path(r'RentaTraje/(?P<id>\d+)/$',modulorenta,name='modulorenta'),
    re_path(r'descripcion/(?P<id>\d+)/$',descripcion,name='descripcion'),
]
