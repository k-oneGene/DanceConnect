from django.db import models
from django.conf import settings
from django.db.models import Q

User = settings.AUTH_USER_MODEL

# Create your models here.


class EventManagerQuerySet(models.query.QuerySet):
    def search(self, query):
        return self.filter(
            Q(creator__username__icontains=query) |
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(start__icontains=query) |
            Q(end__icontains=query)
                ).distinct()


class EventManager(models.Manager):
    def get_queryset(self):
        return EventManagerQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    creator = models.ForeignKey(User, models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True)
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField() # todo: need validation to check start/end is smaller/bigger

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    object = EventManager()

    def __str__(self):
        return f'{self.start} - {self.name}'

    def list_category(self):
        all_cat = ', '.join([category.name for category in self.categories.all()])
        return all_cat
