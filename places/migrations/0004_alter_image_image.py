# Generated by Django 4.2.15 on 2024-08-07 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0003_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='картинка'),
        ),
    ]
