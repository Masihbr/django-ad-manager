# Generated by Django 3.1.5 on 2021-01-28 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='url',
            field=models.URLField(default=''),
        ),
    ]