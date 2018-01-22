from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from profiles.models import Profile
from django.shortcuts import redirect, reverse, HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import User


from profiles.models import Profile
from friends.models import Friend
# Create your views here.


class Friend_Add(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            to_user_id = request.POST.get("to_user")
            to_user = User.objects.get(pk=to_user_id)
            from_user = self.request.user
            friendship, created = Friend.objects.add_friend(from_user, to_user)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Object does not Exist error. User exists?')
            return redirect(reverse('profiles:profile'))


class Friend_Unrequest(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            to_user_id = request.POST.get("to_user")
            to_user = User.objects.get(pk=to_user_id)
            from_user = self.request.user
            Friend.objects.unrequest_friend(from_user, to_user)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Object does not Exist error. User exists?')
            return redirect(reverse('profiles:profile'))

#Accept or Remove request
class Friend_Accept(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        friend_action = request.POST.get("friend_action")
        if friend_action == "accept":
            try:
                from_user_id = request.POST.get("to_user")
                from_user = User.objects.get(pk=from_user_id)
                to_user = self.request.user
                Friend.objects.accept_friend(from_user, to_user)
                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)
            except ObjectDoesNotExist:
                messages.error(self.request, 'Object does not Exist error. User exists?')
                return redirect(reverse('profiles:profile'))
        elif friend_action == "remove":
            try:
                from_user_id = request.POST.get("to_user")
                from_user = User.objects.get(pk=from_user_id)
                to_user = self.request.user
                Friend.objects.remove_friend(from_user, to_user)
                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)
            except ObjectDoesNotExist:
                messages.error(self.request, 'Object does not Exist error. User exists?')
                return redirect(reverse('profiles:profile'))


class Friend_Unfriend(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            to_user_id = request.POST.get("to_user")
            to_user = User.objects.get(pk=to_user_id)
            from_user = self.request.user
            Friend.objects.unfriend_friend(from_user, to_user)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Object does not Exist error. User exists?')
            return redirect(reverse('profiles:profile'))


class Friend_Block(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            to_user_id = request.POST.get("to_user")
            to_user = User.objects.get(pk=to_user_id)
            from_user = self.request.user
            Friend.objects.block_friend(from_user, to_user)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Object does not Exist error. User exists?')
            return redirect(reverse('profiles:profile'))


class Friend_Unblock(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            to_user_id = request.POST.get("to_user")
            to_user = User.objects.get(pk=to_user_id)
            from_user = self.request.user
            Friend.objects.unblock_friend(from_user, to_user)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Object does not Exist error. User exists?')
            return redirect(reverse('profiles:profile'))


class Friend_Logic(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # next_action = request.POST.get("next_action")
        block_action = request.POST.get("block_action")
        print('h===================================')
        print(request.POST)
        if block_action == 'block':
            try:
                to_user_id = request.POST.get("to_user")
                to_user = User.objects.get(pk=to_user_id)
                from_user = self.request.user
                Friend.objects.block_friend(from_user, to_user)
                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)
            except ObjectDoesNotExist:
                messages.error(self.request, 'Object does not Exist error. User exists?')
                return redirect(reverse('profiles:profile'))
            # return redirect(reverse('friends:block'), request=request)
        elif block_action == 'unblock':
            try:
                to_user_id = request.POST.get("to_user")
                to_user = User.objects.get(pk=to_user_id)
                from_user = self.request.user
                Friend.objects.unblock_friend(from_user, to_user)
                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)
            except ObjectDoesNotExist:
                messages.error(self.request, 'Object does not Exist error. User exists?')
                return redirect(reverse('profiles:profile'))
            # return redirect(reverse('friends:unblock'))


class FriendsListView(LoginRequiredMixin, ListView):
    template_name = 'friends/friends_list.html'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user).first().get_friends()


class FriendsRequestedListView(LoginRequiredMixin, ListView):
    template_name = 'friends/friends_requested_list.html'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user).first().get_friend_requested()


class FriendsBlockedListView(LoginRequiredMixin, ListView):
    template_name = 'friends/friends_blocked_list.html'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user).first().get_friend_blocked()


class FriendsMyRequestsListView(LoginRequiredMixin, ListView):
    template_name = 'friends/friends_my_requests_list.html'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user).first().get_friend_my_requests()


