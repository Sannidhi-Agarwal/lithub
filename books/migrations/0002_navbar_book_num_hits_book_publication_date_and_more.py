# Generated by Django 5.1.1 on 2024-10-07 05:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Navbar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('url', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='num_hits',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='publication_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default='False'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='book',
            name='ratings_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='book',
            name='reviews_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date of Review'),
        ),
        migrations.AlterField(
            model_name='user',
            name='account_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='user',
            name='num_books',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='num_friends',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='num_reviews',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, unique='True'),
        ),
    ]
