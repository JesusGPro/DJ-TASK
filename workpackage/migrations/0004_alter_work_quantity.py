# Generated by Django 4.2.16 on 2024-09-16 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workpackage', '0003_work'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='quantity',
            field=models.DecimalField(decimal_places=3, max_digits=30),
        ),
    ]
