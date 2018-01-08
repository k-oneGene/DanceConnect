from django.shortcuts import render, get_object_or_404

from django.views.generic import TemplateView, ListView

import pendulum

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


class MyHomeListView(ListView):
    model = Profile
    template_name = 'myhome.html'

    def get_queryset(self):
        return self.request.user.profile.events.all()

    def get_context_data(self, **kwargs):
        context = super(MyHomeListView, self).get_context_data(**kwargs)

        # todo: START WITH FINISHED THESE AND LINKING TO MY TEMPLATE!

        my_events_all = context['object_list']
        now = pendulum.now()

        # context['recommended_events']
        context['events_going'] = my_events_all.filter(end__gte=now).order_by('start')
        context['past_events'] = my_events_all.filter(end__lt=now).order_by('-start')
        return context
