# Generated by Django 4.2.7 on 2024-04-30 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avidoapp', '0007_alter_messagemodel_creation_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adobjectmodel',
            name='conditions',
            field=models.TextField(blank=True, null=True, verbose_name='Условия работы'),
        ),
        migrations.AlterField(
            model_name='adobjectmodel',
            name='contacts',
            field=models.TextField(blank=True, null=True, verbose_name='Контактная информация работодателя'),
        ),
        migrations.AlterField(
            model_name='adobjectmodel',
            name='requirements',
            field=models.TextField(blank=True, null=True, verbose_name='Требования'),
        ),
        migrations.AlterField(
            model_name='adobjectmodel',
            name='schedule',
            field=models.TextField(blank=True, null=True, verbose_name='График работы'),
        ),
    ]