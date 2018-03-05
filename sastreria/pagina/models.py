from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    user_nombre = models.CharField(max_length = 30, blank = True)
    user_apellido = models.CharField(max_length = 30, blank = True)
    direccion = models.CharField(max_length = 50, blank = True)
    fecha_nacimiento = models.DateField(null = True, blank = True)

    def __str__(self):
        return self.user.username

# Busca en models las diferentes instancias
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
    instance.perfil.save()
