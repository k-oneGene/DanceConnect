from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView, DetailView

from .models import Event

# Create your views here.


class EventListView(ListView):
    def get_queryset(self):
        return Event.objects.all()


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