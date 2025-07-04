# Generated by Django 5.1.3 on 2024-11-29 02:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appEYV', '0010_cliente_email_alter_cliente_id_usuario_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='ID_usuario',
        ),
        migrations.AddField(
            model_name='cliente',
            name='usuario',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='Email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
