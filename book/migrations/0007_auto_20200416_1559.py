# Generated by Django 3.0.5 on 2020-04-16 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_auto_20200413_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.FileField(upload_to='static/home/images/uploads/%Y/%m/'),
        ),
    ]
