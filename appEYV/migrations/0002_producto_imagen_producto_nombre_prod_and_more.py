# Generated by Django 4.2.2 on 2024-10-25 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appEYV', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='Imagen',
            field=models.ImageField(blank=True, null=True, upload_to='app/img/'),
        ),
        migrations.AddField(
            model_name='producto',
            name='nombre_prod',
            field=models.CharField(default='Producto Genérico', max_length=50),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='ID_cliente',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='compra',
            name='ID_compra',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='detalleventa',
            name='NumComprobante',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='factura',
            name='ID_factura',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='mediopago',
            name='ID_pago',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='pago',
            name='ID_pago',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='producto',
            name='ID_prod',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='ID_usuario',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='venta',
            name='Comprobante',
            field=models.CharField(max_length=3),
        ),
    ]
