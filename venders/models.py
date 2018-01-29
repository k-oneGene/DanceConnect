from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.

from events.models import Category


class Vender(models.Model):
    owner = models.ForeignKey(User, models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True)
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)

    image = models.ImageField(upload_to='vender_page', blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # objects = EventManager()

    def __str__(self):
        return f'{self.owner} - {self.name}'

    def list_category(self):
        all_cat = ', '.join([category.name for category in self.categories.all()])
        return all_cat