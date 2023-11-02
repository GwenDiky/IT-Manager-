# Generated by Django 4.2.2 on 2023-09-15 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_profile_experience_years_alter_profile_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='experience',
            field=models.TextField(blank=True, default='Отсутствует', null=True, verbose_name='Опыт работы'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='experience_years',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=2, null=True, verbose_name='Опыт работы (в годах)'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(blank=True, choices=[('-', 'Неопределен'), ('М', 'Мужской'), ('Ж', 'Женский')], max_length=30, null=True, verbose_name='Гендер'),
        ),
    ]