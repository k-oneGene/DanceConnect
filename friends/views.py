from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from profiles.models import Profile
from django.shortcuts import redirect, reverse, HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import User
from notify.signals import notify


from profiles.models import Profile
from friends.models import Friend
# Create your views here.


#TODO: All or most of post are not needed because now I'm doing it through get due to some good reason.

class Friend_Add(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            to_user_id = request.POST.get("to_user")
            to_user = User.objects.get(pk=to_user_id)
            from_user = self.request.user
            Friend.objects.add_friend(from_user, to_user)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Object does not Exist error. User exists?')
            return redirect(reverse('profiles:profile'))

    def get(self, request, *args, **kwargs):
        to_user_id = self.kwargs.get('pk')
        to_user = User.objects.get(pk=to_user_id)
        from_user = self.request.user
        Friend.objects.add_friend(from_user, to_user)


        next = request.session.get('next')
        return HttpResponseRedirect(next)


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

    def get(self, request, *args, **kwargs):
        to_user_id = self.kwargs.get('pk')
        to_user = User.objects.get(pk=to_user_id)
        from_user = self.request.user
        Friend.objects.unrequest_friend(from_user, to_user)
        next = request.session.get('next')
        return HttpResponseRedirect(next)

#Accept or Remove request
class Friend_Accept(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        from_user_id = self.kwargs.get('pk')
        from_user = User.objects.get(pk=from_user_id)
        to_user = self.request.user
        Friend.objects.accept_friend(from_user, to_user)

        # Notify friend request sender
        notify.send(to_user, recipient=from_user, actor=to_user, verb=' has accepted friendship request.', nf_type='friends_all')

        # Notify yourself
        notify.send(from_user, recipient=to_user, actor=from_user, verb=' accepted ', nf_type='friends_accept_self')

        next = request.session.get('next')
        return HttpResponseRedirect(next)


class Friend_Remove(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        from_user_id = self.kwargs.get('pk')
        from_user = User.objects.get(pk=from_user_id)
        to_user = self.request.user
        Friend.objects.remove_friend(from_user, to_user)
        next = request.session.get('next')
        return HttpResponseRedirect(next)


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

    def get(self, request, *args, **kwargs):
        to_user_id = self.kwargs.get('pk')
        to_user = User.objects.get(pk=to_user_id)
        from_user = self.request.user
        Friend.objects.unfriend_friend(from_user, to_user)
        next = request.session.get('next')
        return HttpResponseRedirect(next)


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

    def get(self, request, *args, **kwargs):
        to_user_id = self.kwargs.get('pk')
        to_user = User.objects.get(pk=to_user_id)
        from_user = self.request.user
        Friend.objects.block_friend(from_user, to_user)
        next = request.session.get('next')
        return HttpResponseRedirect(next)


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

    def get(self, request, *args, **kwargs):
        to_user_id = self.kwargs.get('pk')
        to_user = User.objects.get(pk=to_user_id)
        from_user = self.request.user
        Friend.objects.unblock_friend(from_user, to_user)
        next = request.session.get('next')
        return HttpResponseRedirect(next)


class Friend_Logic(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        friend_action = request.POST.get("friend_action")
        block_action = request.POST.get("block_action")

        to_user_id = request.POST.get("to_user")
        next = request.POST.get('next', '/')
        request.session['next'] = next

        if block_action == 'block':
            return redirect(reverse('friends:block', kwargs={'pk': to_user_id}))
        elif block_action == 'unblock':
            return redirect(reverse('friends:unblock', kwargs={'pk': to_user_id}))

        if friend_action == 'add':
            return redirect(reverse('friends:add', kwargs={'pk': to_user_id}))
        elif friend_action == 'requested':
            return redirect(reverse('friends:unrequest', kwargs={'pk': to_user_id}))
        elif friend_action == 'accept':
            return redirect(reverse('friends:accept', kwargs={'pk': to_user_id}))
        elif friend_action == 'remove':
            return redirect(reverse('friends:remove', kwargs={'pk': to_user_id}))
        elif friend_action == 'unfriend':
            return redirect(reverse('friends:unfriend', kwargs={'pk': to_user_id}))




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


