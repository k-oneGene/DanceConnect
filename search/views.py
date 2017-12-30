from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from events.models import Event
from profiles.models import Profile

# Create your views here.

class SearchEventsListview(ListView):
    model = Event
    template_name = 'search/searchevents_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SearchEventsListview, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        qs = context['object_list']
        if query:
            qs = qs.search(query)
        context['object_list'] = qs
        return context


class SearchProfilesListview(ListView):
    model = Profile
    template_name = 'search/searchprofiles_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProfilesListview, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        qs = context['object_list'] # Profile.objects.all(), but ListView auto does this.
        if query:
            qs = qs.search(query)
        context['object_list'] = qs
        return context