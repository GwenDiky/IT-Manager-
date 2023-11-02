# Generated by Django 4.2.2 on 2023-10-15 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_alter_profile_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(blank=True, choices=[('М', 'Мужской'), ('-', 'Неопределен'), ('Ж', 'Женский')], max_length=30, null=True, verbose_name='Гендер'),
        ),
    ]