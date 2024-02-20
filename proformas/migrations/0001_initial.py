# Generated by Django 5.0 on 2023-12-29 08:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proformas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_proforma', models.CharField(max_length=5, unique=True)),
                ('cliente', models.CharField(max_length=50)),
                ('fecha', models.DateField()),
                ('importe_total', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ItemProforma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=5)),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('importe', models.DecimalField(decimal_places=2, max_digits=10)),
                ('proforma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proformas.proformas')),
            ],
        ),
    ]
