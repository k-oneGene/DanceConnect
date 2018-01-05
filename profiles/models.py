from django.db import models
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
import os

from events.models import Category

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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # activated = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=False, blank=False)
    gender = models.CharField(max_length=40)
    address = models.CharField(max_length=120)

    categories = models.ManyToManyField(Category, blank=True)
    bio = models.TextField()
    image = models.ImageField(upload_to=profile_name_path, storage=OverwriteStorage(), blank=True, null=True)

    teacher = models.BooleanField()

    objects = ProfileManager() # adding to Model.objects.all()

    def __str__(self):
        return self.user.username

    def list_category(self):
        # all_cat = ''
        # for category in self.categories.all():
        #     all_cat += category.name + ' '
        all_cat = ', '.join([category.name for category in self.categories.all()])
        return all_cat
