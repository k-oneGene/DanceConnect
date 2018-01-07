from django.shortcuts import render, get_object_or_404

from django.views.generic import TemplateView

from events.models import Event
from profiles.models import Profile

# Create your views here.


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events_list'] = Event.objects.filter(type__exact='event').order_by('-start')[0:4]
        context['profiles_list'] = Profile.objects.order_by('-user__date_joined')[0:4]
        context['festivals_list'] = Event.objects.filter(type__exact='festival').order_by('-start')[0:4]
        context['teachers_list'] = Profile.objects.filter(teacher=True).order_by('-user__date_joined')[0:4]
        return context


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