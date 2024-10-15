# Generated by Django 5.1.1 on 2024-10-15 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_book_cover_book_isbn13_alter_book_isbn_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
