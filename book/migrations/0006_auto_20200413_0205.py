# Generated by Django 3.0.5 on 2020-04-13 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_auto_20200413_0203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.FileField(upload_to='uploads/%Y/%m/%d/'),
        ),
    ]