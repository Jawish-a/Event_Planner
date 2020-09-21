from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.utils.timezone import timedelta, timezone
import uuid

#########################################################################
#       user model                                                      #
#########################################################################

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'user_profile_pics', null=True, blank=True)
    bio = models.TextField(max_length=200, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    
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


#########################################################################
#       ticket model                                                    #
#########################################################################

class Ticket(models.Model):
    number = models.UUIDField(default=uuid.uuid4, editable=False)
    tickets = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets', related_query_name='event')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets', related_query_name='user')
    def __str__(self):
        return f"{self.event.name} | {self.user.first_name} {self.user.last_name}"


#########################################################################
#       follow model                                                    #
#########################################################################

class Follower(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('follower', 'following')

    # def __str__(self):
    #     return u'%s follows %s' % (self.follower, self.following)
    # def __str__(self):
    #     return self.following.username