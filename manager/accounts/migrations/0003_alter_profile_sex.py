# Generated by Django 4.2.2 on 2023-09-15 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(blank=True, choices=[('М', 'Мужской'), ('-', 'Неопределен'), ('Ж', 'Женский')], max_length=30, null=True, verbose_name='Гендер'),
        ),
    ]
