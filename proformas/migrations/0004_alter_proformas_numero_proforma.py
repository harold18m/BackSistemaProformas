# Generated by Django 5.0 on 2024-01-04 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proformas', '0003_alter_proformas_importe_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proformas',
            name='numero_proforma',
            field=models.CharField(max_length=7, unique=True),
        ),
    ]
