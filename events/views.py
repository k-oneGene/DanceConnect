from django.shortcuts import render, get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, reverse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Event, Category
from .forms import EventForm
from profiles.models import Profile

# Create your views here.

# ==============
# Events related
# ==============


class EventListView(ListView):
    def get_queryset(self):
        return Event.objects.all().order_by('-start')

    # def get_context_data(self, **kwargs):
    #     context = super(EventListView, self).get_context_data(**kwargs)
    #     context['events_going'] = self.request.user.profile.events.all()
    #     return context


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
    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            event = context['event']
            is_going = False
            if event in self.request.user.profile.events.all():
                is_going = True
            context['is_going'] = is_going
        return context


class EventCreateView(LoginRequiredMixin, CreateView):
    form_class = EventForm
    template_name = 'events/event_create.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.creator = self.request.user
        messages.success(self.request, 'Your event has been created')
        return super(EventCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('events:detail', kwargs={'pk': self.object.id})


#TODO: NEED to check if other users can edit other people's events
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_edit.html'

    def get_form_kwargs(self):
        kwargs = super(EventUpdateView, self).get_form_kwargs()
        current_event = self.get_object()
        kwargs['initial']['start'] = str(current_event.start).replace(' ', 'T')[0:16]
        kwargs['initial']['end'] = str(current_event.end).replace(' ', 'T')[0:16]
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        current_event = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy('events:detail', kwargs={'pk': self.get_object().id})


class EventDeleteView(DeleteView):
    model = Event
    template_name = 'events/event_delete.html'
    success_url = reverse_lazy('events:list')

    def delete(self, request, *args, **kwargs):
        success_message = 'Event has been deleted'
        messages.error(self.request, success_message)
        return super(EventDeleteView, self).delete(request, *args, **kwargs)


# ==============
# Category related
# ==============


class CategoryListView(ListView):
    model = Category


class CategoryListInfoListView(DetailView):
    model = Category
    template_name = 'events/category_list_info_list.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryListInfoListView, self).get_context_data(**kwargs)
        category = self.get_object()
        context['events_list'] = Event.objects.filter(categories=category).order_by('-start')
        context['profiles_list'] = Profile.objects.filter(teacher=True,teacher_categories=category)
        return context


class EventGoingToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        event_to_toggle = request.POST.get("eventID")
        event_, is_following = Profile.objects.toggle_event(request.user.profile, event_to_toggle)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

# return redirect(reverse("events:detail", kwargs={'pk': event_.id})) #redirect(f"{profile_.user.username}/")