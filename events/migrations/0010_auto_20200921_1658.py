# Generated by Django 3.1.1 on 2020-09-21 13:58

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0009_follower'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follower',
            old_name='follower',
            new_name='user_follower',
        ),
        migrations.RenameField(
            model_name='follower',
            old_name='following',
            new_name='user_following',
        ),
        migrations.AlterUniqueTogether(
            name='follower',
            unique_together={('user_follower', 'user_following')},
        ),
    ]