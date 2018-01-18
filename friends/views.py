from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from profiles.models import Profile
from django.shortcuts import redirect, reverse, HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from profiles.models import Profile
# Create your views here.


class Friend_Add(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            event_to_toggle = request.POST.get("eventID")
            event_, is_following = Profile.objects.toggle_event(request.user.profile, event_to_toggle)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Please add details to manage events')
            return redirect(reverse('profiles:profile'))



class Friend_Accept(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            event_to_toggle = request.POST.get("eventID")
            event_, is_following = Profile.objects.toggle_event(request.user.profile, event_to_toggle)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Please add details to manage events')
            return redirect(reverse('profiles:profile'))


class Friend_Block(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            event_to_toggle = request.POST.get("eventID")
            event_, is_following = Profile.objects.toggle_event(request.user.profile, event_to_toggle)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Please add details to manage events')
            return redirect(reverse('profiles:profile'))




class Friend_Unfriend(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            event_to_toggle = request.POST.get("eventID")
            event_, is_following = Profile.objects.toggle_event(request.user.profile, event_to_toggle)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Please add details to manage events')
            return redirect(reverse('profiles:profile'))



class Friend_Delete_Request(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            event_to_toggle = request.POST.get("eventID")
            event_, is_following = Profile.objects.toggle_event(request.user.profile, event_to_toggle)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Please add details to manage events')
            return redirect(reverse('profiles:profile'))





class FriendsListView(LoginRequiredMixin, ListView):
    template_name = 'friends/friends_list.html'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user).first().get_friends()
