from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView

# Create your views here.
from .models import Vender
from events.models import Event


class VenderListView(ListView):
    def get_queryset(self):
        return Vender.objects.all()


class VenderDetailView(DetailView):
    model = Vender

    def get_context_data(self, **kwargs):
        context = super(VenderDetailView, self).get_context_data(**kwargs)
        vender = self.get_queryset()[0]
        context['events_list'] = vender.events.all()
        return context
