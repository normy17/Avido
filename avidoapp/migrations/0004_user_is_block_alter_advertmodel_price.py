# Generated by Django 4.2.7 on 2024-04-18 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avidoapp', '0003_rename_images_imagemodel_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_block',
            field=models.BooleanField(default=False, verbose_name='Блокировка'),
        ),
        migrations.AlterField(
            model_name='advertmodel',
            name='price',
            field=models.IntegerField(verbose_name='Цена'),
        ),
    ]