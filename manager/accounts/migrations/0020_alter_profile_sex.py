# Generated by Django 4.2.2 on 2023-09-21 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_remove_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(blank=True, choices=[('-', 'Неопределен'), ('Ж', 'Женский'), ('М', 'Мужской')], max_length=30, null=True, verbose_name='Гендер'),
        ),
    ]
