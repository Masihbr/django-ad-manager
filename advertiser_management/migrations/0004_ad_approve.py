# Generated by Django 3.1.5 on 2021-02-01 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0003_click_view'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='approve',
            field=models.BooleanField(default=False),
        ),
    ]
