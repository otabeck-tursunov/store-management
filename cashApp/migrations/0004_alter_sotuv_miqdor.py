# Generated by Django 4.2.2 on 2023-06-26 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashApp', '0003_alter_chiqim_miqdor_alter_maosh_miqdor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sotuv',
            name='miqdor',
            field=models.PositiveIntegerField(),
        ),
    ]
