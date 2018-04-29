# Generated by Django 2.0.1 on 2018-04-29 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pagina', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Citas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CitaHora', models.CharField(choices=[('hora1', '08:00:00'), ('hora2', '09:00:00'), ('hora3', '10:00:00'), ('hora4', '11:00:00'), ('hora5', '12:00:00'), ('hora6', '13:00:00'), ('hora7', '14:00:00'), ('hora8', '15:00:00'), ('hora9', '16:00:00'), ('hora10', '17:00:00'), ('hora11', '18:00:00')], default=1, max_length=9)),
                ('CitaFecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Purchase_at', models.DateTimeField(auto_now_add=True)),
                ('tx', models.CharField(max_length=250)),
                ('purchaser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sastrerias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=30)),
                ('Localizacion', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='TuxedosCompletos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tipo', models.CharField(max_length=30)),
                ('Color', models.CharField(max_length=30)),
                ('TipodeTela', models.CharField(max_length=30)),
                ('PrecioV', models.DecimalField(decimal_places=2, max_digits=10)),
                ('PrecioR', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Descripcion', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='purchase',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagina.TuxedosCompletos'),
        ),
        migrations.AddField(
            model_name='citas',
            name='LugarCita',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagina.Sastrerias'),
        ),
        migrations.AddField(
            model_name='citas',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]