# Generated by Django 3.0.5 on 2020-04-18 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0011_auto_20200418_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='description',
            field=models.TextField(default='test'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='book.Review'),
        ),
    ]