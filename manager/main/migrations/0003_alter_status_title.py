# Generated by Django 4.2.2 on 2023-10-18 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_comment_id_alter_company_id_alter_status_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='title',
            field=models.CharField(choices=[('+/-', 'В процессе'), ('+', 'Завершено'), ('-', 'Не завершено')], default='-', max_length=30, verbose_name='Завершенность'),
        ),
    ]
