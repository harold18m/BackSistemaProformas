# Generated by Django 5.0 on 2023-12-29 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proformas', '0002_proformas_hora_alter_proformas_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proformas',
            name='importe_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
