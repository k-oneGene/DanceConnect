from django.db import models
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
import os

from events.models import Category, Event
from friends.models import Friend

User = settings.AUTH_USER_MODEL


def profile_name_path(instance, filename):
    path = "profile_list"
    name, file_extension = os.path.splitext(filename)
    new_filename = str(instance.id) + file_extension
    return os.path.join(path, new_filename)


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class ProfileManagerQuerySet(models.query.QuerySet):
    def search(self, query): #Profiles.objects.all().search(query) OR Profiles.objects.filter().search(query)
        return self.filter(
            Q(user__username__icontains=query)|
            Q(date_of_birth__icontains=query)|
            Q(categories__name__icontains=query)
        ).distinct()
        # return self.filter(user__username__contains=query)


class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileManagerQuerySet(self.model, using=self._db)

    def search(self, query): #Profile.objects.search()
        return self.get_queryset().search(query)

    def toggle_event(self, requested_user, event_to_toggle):
        event_ = Event.objects.get(id=event_to_toggle)
        user = requested_user
        is_going = False
        if user in event_.profiles.all():
            event_.profiles.remove(user)
        else:
            event_.profiles.add(user)
            is_going = True
        return event_, is_going


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # activated = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=False, blank=False)
    gender = models.CharField(max_length=40)
    address = models.CharField(max_length=120)

    categories = models.ManyToManyField(Category, blank=True, related_name='categories')
    bio = models.TextField()
    image = models.ImageField(upload_to='profile_list', blank=True, null=True)

    # For teaching
    teacher = models.BooleanField()
    teacher_categories = models.ManyToManyField(Category, blank=True, related_name='teaching')

    events = models.ManyToManyField(Event, blank=True, related_name='profiles')

    # friends = models.ManyToManyField(User, through='Friendship', through_fields=('from_user', 'to_user'), related_name='friends', symmetrical=False, blank=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    def list_category(self):
        # all_cat = ''
        # for category in self.categories.all():
        #     all_cat += category.name + ' '
        all_cat = ', '.join([category.name for category in self.categories.all()])
        return all_cat

    def get_friends(self):
        return Friend.objects.filter((Q(from_user=self.user) | Q(to_user=self.user)) & Q(status='friend'))

    def get_friend_my_requests(self):
        return Friend.objects.filter(Q(from_user=self.user) & Q(status='requested'))

    def get_friend_requested(self):
        return Friend.objects.filter(Q(to_user=self.user) & Q(status='requested'))

    def get_friend_blocked(self):
        return Friend.objects.filter(Q(from_user=self.user) & Q(status='blocked'))

    def get_friends_all_list(self):
        return Friend.objects.filter((Q(from_user=self.user)))