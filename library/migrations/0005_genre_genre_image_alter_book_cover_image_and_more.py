# Generated by Django 4.2.17 on 2024-12-09 18:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_book_file_book_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='genre_image',
            field=models.ImageField(null=True, upload_to='genre_images/'),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(upload_to='cover_images/'),
        ),
        migrations.AlterField(
            model_name='book',
            name='file',
            field=models.FileField(blank=True, default=datetime.datetime(2024, 12, 9, 18, 44, 29, 668468, tzinfo=datetime.timezone.utc), upload_to='books/'),
            preserve_default=False,
        ),
    ]
