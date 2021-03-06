# Generated by Django 3.1.1 on 2020-09-21 14:26

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0010_auto_20200921_1658'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follower',
            old_name='user_follower',
            new_name='follower',
        ),
        migrations.RenameField(
            model_name='follower',
            old_name='user_following',
            new_name='following',
        ),
        migrations.AlterUniqueTogether(
            name='follower',
            unique_together={('follower', 'following')},
        ),
    ]
