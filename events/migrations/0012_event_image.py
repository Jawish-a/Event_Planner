# Generated by Django 3.1.1 on 2020-09-22 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20200921_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='events_featured_images'),
        ),
    ]
