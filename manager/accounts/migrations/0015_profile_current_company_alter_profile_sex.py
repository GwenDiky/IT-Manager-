# Generated by Django 4.2.2 on 2023-09-15 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_profile_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='current_company',
            field=models.CharField(blank=True, default='В поиске работы', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(blank=True, choices=[('-', 'Неопределен'), ('Ж', 'Женский'), ('М', 'Мужской')], max_length=30, null=True, verbose_name='Гендер'),
        ),
    ]