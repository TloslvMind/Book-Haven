# Generated by Django 5.1.4 on 2024-12-08 16:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_book_cover_image_alter_book_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
