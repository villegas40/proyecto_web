# sastreria
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

# Create your models here.
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    user_name = models.CharField(max_length = 30, blank = True)
    user_last = models.CharField(max_length = 30, blank = True)
    email = models.EmailField(blank = True)
    location = models.CharField(max_length = 30, blank = True)
    birth_date = models.DateField(null = True, blank = True)

    def __str__(self):
        return self.user.username

# Buscar en models las diferentes instancias
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
    instance.perfil.save()

# Modelo de los productos del carrito de compras
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length = 100, blank=True)
    precio = models.DecimalField(max_digits=6,decimal_places=2)
    image_url = models.CharField(max_length=100, blank=True)
    cantitad = models.IntegerField()
    categoria = models.CharField(max_length=50, blank=True)
    fecha_alta = models.DateTimeField(default=datetime.now, blank=True)
    color = models.CharField(max_length=50, default = 'negro')
    descripcion = models.CharField(max_length=200, default='')


    def __str__(self):
        return self.nombre_producto

class Sastrerias(models.Model):
    Nombre = models.CharField(max_length=30)
    Localizacion = models.CharField(max_length=40)

    def __str__(self):
        return self.Nombre


class Citas(models.Model):
    CitaFecha = models.DateField()
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    LugarCita = models.ForeignKey(Sastrerias,on_delete=models.CASCADE)
    CitaHora = models.CharField(choices=(("hora1",("08:00:00")),
                                        ("hora2",("09:00:00")),
                                        ("hora3",("10:00:00")),
                                        ("hora4",("11:00:00")),
                                        ("hora5",("12:00:00")),
                                        ("hora6",("13:00:00")),
                                        ("hora7",("14:00:00")),
                                        ("hora8",("15:00:00")),
                                        ("hora9",("16:00:00")),
                                        ("hora10",("17:00:00")),
                                        ("hora11",("18:00:00"))),default =1,max_length=9)
class Purchase(models.Model):
    resource = models.ManyToManyField(Product)
    purchaser = models.ForeignKey(User,on_delete=models.CASCADE)
    Purchase_at = models.DateTimeField(auto_now_add=True)
    tx = models.CharField(max_length=250)
