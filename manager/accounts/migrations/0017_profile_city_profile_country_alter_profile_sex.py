# Generated by Django 4.2.2 on 2023-09-15 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_profile_current_company_alter_profile_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(default='Беларусь', max_length=50, verbose_name='Страна'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(blank=True, choices=[('-', 'Неопределен'), ('Ж', 'Женский'), ('М', 'Мужской')], max_length=30, null=True, verbose_name='Гендер'),
        ),
    ]