# Generated by Django 4.2.2 on 2023-10-18 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0032_alter_profile_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(blank=True, choices=[('М', 'Мужской'), ('Ж', 'Женский'), ('-', 'Неопределен')], max_length=30, null=True, verbose_name='Гендер'),
        ),
    ]