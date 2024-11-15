# Generated by Django 4.2.16 on 2024-09-14 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_project_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eur_sar', models.DecimalField(decimal_places=2, default=4.16, max_digits=10)),
                ('usd_sar', models.DecimalField(decimal_places=2, default=3.75, max_digits=10)),
                ('eur_usd', models.DecimalField(decimal_places=2, default=1.11, max_digits=10)),
            ],
        ),
    ]
