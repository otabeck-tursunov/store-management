# Generated by Django 4.2.2 on 2023-06-19 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mahsulot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=150)),
                ('brand', models.CharField(blank=True, max_length=150, null=True)),
                ('rasm', models.ImageField(blank=True, null=True, upload_to='mahsulot')),
                ('batafsil', models.TextField(blank=True, null=True)),
                ('narx1', models.FloatField()),
                ('narx2', models.FloatField()),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ombor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=150)),
                ('tel', models.CharField(blank=True, max_length=13, null=True)),
                ('manzil', models.CharField(max_length=255)),
                ('rasm', models.ImageField(blank=True, null=True, upload_to='filial')),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Mahsulot_tarqatish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miqdor', models.FloatField()),
                ('sana', models.DateField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('mahsulot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tarqatmalar', to='mainApp.mahsulot')),
                ('ombor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mahsulot_tarqatmalar', to='mainApp.ombor')),
            ],
        ),
    ]
