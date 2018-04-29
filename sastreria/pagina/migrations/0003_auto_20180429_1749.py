# Generated by Django 2.0.1 on 2018-04-29 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0002_auto_20180429_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Color',
            field=models.CharField(default='negro', max_length=30),
        ),
        migrations.AddField(
            model_name='product',
            name='Descripcion',
            field=models.CharField(default='chido', max_length=200),
        ),
        migrations.AddField(
            model_name='product',
            name='PrecioR',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
        ),
        migrations.AddField(
            model_name='product',
            name='TipodeTela',
            field=models.CharField(default='algodon', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagina.Product'),
        ),
        migrations.DeleteModel(
            name='TuxedosCompletos',
        ),
    ]