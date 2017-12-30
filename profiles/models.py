from django.db import models
from django.conf import settings
from django.db.models import Q

from events.models import Category

# Create your models here.

User = settings.AUTH_USER_MODEL


class ProfileManagerQuerySet(models.query.QuerySet):
    def search(self, query): #Profiles.objects.all().search(query) OR Profiles.objects.filter().search(query)
        return self.filter(
            Q(user__username__icontains=query)|
            Q(date_of_birth__icontains=query)
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
    address = models.CharField(max_length=120)

    categories = models.ManyToManyField(Category, blank=True)
    # todo: student/teacher/status?
    bio = models.TextField()

    objects = ProfileManager() # adding to Model.objects.all()

    def __str__(self):
        return self.user.username

    def list_category(self):
        # all_cat = ''
        # for category in self.categories.all():
        #     all_cat += category.name + ' '
        all_cat = ', '.join([category.name for category in self.categories.all()])
        return all_cat
