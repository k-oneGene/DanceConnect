from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView, DetailView

from .models import Event, Category
from profiles.models import Profile

# Create your views here.


class EventListView(ListView):
    def get_queryset(self):
        return Event.objects.all().order_by('-start')


class EventDetailView(DetailView):
    model = Event

    """
    # get_query expects queryset to be returned not model. (Different to what i see on 2:43:39)
    def get_queryset(self, **kwargs):
        print("hi")
        print(self.kwargs.get('pk'))
        obj = get_object_or_404(Event, id=self.kwargs.get('pk'))
        print(type(obj))
        return obj
        # return Event.objects.filter(id)
    """


class CategoryListView(ListView):
    model = Category


class CategoryListInfoListView(DetailView):
    model = Category
    template_name = 'events/category_list_info_list.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryListInfoListView, self).get_context_data(**kwargs)
        category = self.get_object()
        context['events_list'] = Event.objects.filter(categories=category).order_by('-start')
        context['profiles_list'] = Profile.objects.filter(categories=category)
        return context

