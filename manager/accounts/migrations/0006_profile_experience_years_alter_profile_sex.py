# Generated by Django 4.2.2 on 2023-09-15 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_profile_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='experience_years',
            field=models.TextField(blank=True, default=0, null=True, verbose_name='Опыт работы'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(blank=True, choices=[('Ж', 'Женский'), ('-', 'Неопределен'), ('М', 'Мужской')], max_length=30, null=True, verbose_name='Гендер'),
        ),
    ]
