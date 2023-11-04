# Generated by Django 4.2.2 on 2023-06-19 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mainApp', '0001_initial'),
        ('userApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sotuv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miqdor', models.FloatField()),
                ('sana', models.DateField()),
                ('deleted', models.BooleanField(default=False)),
                ('mahsulot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sotuvlar', to='mainApp.mahsulot')),
                ('ombor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sotuvlar', to='mainApp.ombor')),
                ('xodim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sotuvlar', to='userApp.xodim')),
            ],
        ),
        migrations.CreateModel(
            name='Maosh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miqdor', models.IntegerField()),
                ('izoh', models.TextField(blank=True, null=True)),
                ('sana', models.DateField()),
                ('deleted', models.BooleanField(default=False)),
                ('xodim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maoshlar', to='userApp.xodim')),
            ],
        ),
        migrations.CreateModel(
            name='Chiqim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('izoh', models.TextField()),
                ('miqdor', models.IntegerField()),
                ('sana', models.DateField()),
                ('deleted', models.BooleanField(default=False)),
                ('ombor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chiqimlar', to='mainApp.ombor')),
            ],
        ),
    ]