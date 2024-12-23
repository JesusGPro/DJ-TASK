# Generated by Django 4.2.16 on 2024-09-13 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tasks', '0003_alter_project_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('denomination', models.TextField(max_length=255)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('currency', models.CharField(choices=[('EUR', 'Euros'), ('USD', 'Dollars'), ('SAR', 'SAR'), ('No currency', 'No currency')], max_length=20)),
                ('unit', models.CharField(default='nr', max_length=5)),
                ('tag', models.CharField(choices=[('work', 'Work'), ('manpower', 'Manpower'), ('material', 'Material'), ('machinery', 'Machinery'), ('canon', 'Canon'), ('subcontract', 'Subcontract'), ('other', 'Other'), ('overhead', 'Overhead')], max_length=30)),
                ('reference', models.CharField(blank=True, max_length=30, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.project')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='LNNN.NNN', max_length=20, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('unit', models.CharField(max_length=5)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('currency', models.CharField(choices=[('EUR', 'Euros'), ('USD', 'Dollars'), ('SAR', 'SAR'), ('No currency', 'No currency')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TaskComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=3, max_digits=20)),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prices.price')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prices.task')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='components',
            field=models.ManyToManyField(through='prices.TaskComponent', to='prices.price'),
        ),
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.project'),
        ),
    ]
