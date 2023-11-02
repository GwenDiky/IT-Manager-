# Generated by Django 4.2.2 on 2023-09-15 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_profile_current_company_alter_profile_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='current_company',
            field=models.CharField(default='В поиске работы', max_length=100, verbose_name='Текущая работа'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(blank=True, choices=[('Ж', 'Женский'), ('-', 'Неопределен'), ('М', 'Мужской')], max_length=30, null=True, verbose_name='Гендер'),
        ),
    ]