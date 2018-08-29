from django.shortcuts import render, get_object_or_404

from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect, reverse
from django.core.exceptions import ObjectDoesNotExist

import pendulum

from events.models import Event
from profiles.models import Profile

# Create your views here.


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events_list'] = Event.objects.filter(type__exact='event').order_by('-start')[0:4]
        #TODO: Temporarily filtering teachers to make it look better for demo.
        context['profiles_list'] = Profile.objects.filter(teacher=False).order_by('-user__date_joined')[0:4]
        context['festivals_list'] = Event.objects.filter(type__exact='festival').order_by('-start')[0:4]
        context['teachers_list'] = Profile.objects.filter(teacher=True).order_by('-user__date_joined')[0:4]
        return context


class MyHomeListView(ListView):
    # model = Profile
    template_name = 'myhome.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.request.user.profile
            return super(MyHomeListView, self).dispatch(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return redirect(reverse('profiles:profile'))

    def get_queryset(self):
        return self.request.user.profile.events.all()

    def get_context_data(self, **kwargs):
        context = super(MyHomeListView, self).get_context_data(**kwargs)

        # todo: START WITH FINISHED THESE AND LINKING TO MY TEMPLATE!

        my_events_all = context['object_list']
        now = pendulum.now()

        # context['recommended_events']
        context['events_going'] = my_events_all.filter(end__gte=now).order_by('start')[0:3]
        context['past_events'] = my_events_all.filter(end__lt=now).order_by('-start')[0:3]
        return context
