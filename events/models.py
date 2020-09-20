from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.utils.timezone import timedelta, timezone

#########################################################################
#       user model                                                      #
#########################################################################

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'user_profile_pics', null=True, blank=True)
    bio = models.TextField(max_length=200, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#########################################################################
#       category model                                                  #
#########################################################################

class Category(models.Model):
    name = models.CharField(max_length=191)

    def __str__(self):
        return self.name


#########################################################################
#       event model                                                     #
#########################################################################

class Event(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=500)
    country = models.CharField(max_length=90)
    city = models.CharField(max_length=40)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    duration = models.CharField(max_length=40, null=True, blank=True)
    seats = models.PositiveIntegerField()
    location = models.CharField(max_length=191, default="Virtual")
    category = models.ManyToManyField(Category, related_name='events', related_query_name='categories')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events', related_query_name='organizer')
    def __str__(self):
        return self.name

# calculate the duration from the date or time fields
@receiver(pre_save, sender=Event)
def get_duration(instance, *args, **kwargs):
    if instance.end_date > instance.start_date:
        instance.duration = f"{(instance.end_date - instance.start_date).days} Days"
    instance.duration = f"All Day"

