from django.db import models
from django.conf import settings
from django.db.models import Q
from django.http import Http404
from notify.signals import notify
from django.shortcuts import reverse

from django.core.exceptions import ValidationError
from .exceptions import AlreadyExistsError, AlreadyFriendsError


User = settings.AUTH_USER_MODEL

# Create your models here.

RELATIONSHIP_STATUSES = (('requested', 'requested'), ('friend', 'friend'), ('blocked', 'blocked'))


# Use FriendManager Methods. It contains validation logic. Model methods mainly contain error with interaction with database.
class FriendManager(models.Manager):

    def add_friend(self, from_user, to_user, message=None):
        """ Create a friendship request """
        if from_user == to_user:
            raise ValidationError("Can not friend yourself.")

        if message is None:
            message = ''

        Friend.friend_add(from_user=from_user, to_user=to_user)

        # if created is False:
        #     raise AlreadyExistsError("Friendship already requested")

        # if message:
        #     request.message = message
        #     request.save()


    def unrequest_friend(self, from_user, to_user):
        Friend.friend_unrequest(from_user=from_user, to_user=to_user)

    def accept_friend(self, from_user, to_user):
        Friend.friend_accept(from_user=from_user, to_user=to_user)

    def unfriend_friend(self, from_user, to_user):
        Friend.friend_unfriend(from_user=from_user, to_user=to_user)

    def remove_friend(self, from_user, to_user):
        Friend.friend_remove(from_user=from_user, to_user=to_user)

    def block_friend(self, from_user, to_user):
        Friend.friend_block(from_user=from_user, to_user=to_user)

    def unblock_friend(self, from_user, to_user):
        Friend.friend_unblock(from_user=from_user, to_user=to_user)

class Friend(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user+')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user+')
    status = models.CharField(max_length=50, choices=RELATIONSHIP_STATUSES)
    blocked = models.BooleanField(blank=True, default=False)
    # req_message
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = FriendManager()

    def __str__(self):
        #TODO: Hmm, original way is better. I need another way of returning for message "to user" list on messages/create/ page. This is more of temp fix.
        return f'{self.from_user.username}_to_{self.to_user.username}_{self.status}'
        # return f'{self.to_user.username}'

    # Am I blocked?, Check if I am blocked.
    @staticmethod
    def blocked_status(from_user, to_user):
        try:
            friendship_rev = Friend.objects.get(from_user=to_user, to_user=from_user)
            if friendship_rev.blocked:
                return True
            return False
        except Friend.DoesNotExist:
            return False


    @staticmethod
    def friend_make_status(from_user, to_user, status):
        friendship, create = Friend.objects.get_or_create(from_user=from_user, to_user=to_user)
        friendship.status = status
        friendship.save()


    """
    djinn makes request to adds peter
    """
    @staticmethod
    def friend_add(from_user, to_user, status='requested'):
        # Check if I am blocked first
        try:
            friendship_rev = Friend.objects.get(from_user=to_user, to_user=from_user)
            if friendship_rev.blocked:
                return 'Person has blocked.'
            if friendship_rev.status == 'requested':
                Friend.friend_make_status(from_user, to_user, status='friend')
                Friend.friend_make_status(to_user, from_user, status='friend')

                # Notify friend request sender
                notify.send(to_user, recipient=from_user, actor=to_user, verb=' has accepted friendship request.', nf_type='friends_all')
                # Notify yourself
                # TODO: Maybe change this later somewhere for better message (nf_type and template)
                notify.send(from_user, recipient=to_user, actor=from_user, verb=' accepted ', nf_type='friends_accept_self')


        except Friend.DoesNotExist:
            pass
        friendship, created = Friend.objects.get_or_create(from_user=from_user, to_user=to_user)
        if created:
            friendship.status = status
            friendship.save()
            # Jin addeds Amy
            # (actor=Who, verb=What?,
            notify.send(from_user, recipient=to_user, actor=from_user, verb=' has sent friendship requested. ', nf_type='friends_add' , actor_url_text=reverse('profiles:profile'))





    @staticmethod
    def friend_unrequest(from_user, to_user):
        try:
            friendship = Friend.objects.get(Q(from_user=from_user) & Q(to_user=to_user))
            if friendship.status == 'requested':
                friendship.delete()
        except Friend.DoesNotExist:
            # raise Http404('Can not find such request to unrequest')
            pass

    """
    peter decides to accept djinn as friend.
    Creates relationship other way too automatically.
    (Or raise http404 error if this was called and there was no friend request)
    """
    @staticmethod
    def friend_accept(from_user, to_user):
        try:
            friendship = Friend.objects.get(Q(from_user=from_user) & Q(to_user=to_user))
            if friendship.status == 'requested':
                friendship.status = 'friend'
                friendship.save()
                # Add relationship other way
                Friend.friend_make_status(to_user, from_user, status='friend')
        except Friend.DoesNotExist:
            # raise Http404('Can not find such request to accept')
            pass
        return friendship

    #Removes friendship request.
    @staticmethod
    def friend_remove(from_user, to_user):
        try:
            friendship = Friend.objects.get(Q(from_user=from_user) & Q(to_user=to_user))
            if friendship.status == 'requested':
                friendship.delete()
        except Friend.DoesNotExist:
            # raise Http404('Can not find such request to remove.')
            pass
        return friendship

    @staticmethod
    def friend_unfriend(from_user, to_user):
        try:
            friendship = Friend.objects.get(Q(from_user=from_user) & Q(to_user=to_user))
            if friendship.status == 'friend':
                friendship.delete()
                # Delete friendship other way.
                friendship_reverse = Friend.objects.get(Q(to_user=from_user) & Q(from_user=to_user))
                friendship_reverse.delete()
        except Friend.DoesNotExist:
            # raise Http404('Can not find such request to unfriend.')
            pass

    @staticmethod
    def friend_block(from_user, to_user):
        try:
            friendship, created = Friend.objects.get_or_create(from_user=from_user, to_user=to_user)
            if friendship.blocked is False:
                friendship.blocked = True
                friendship.save()
        except Friend.DoesNotExist:
            raise Http404('Can not find such friend to block.')

    @staticmethod
    def friend_unblock(from_user, to_user):
        try:
            friendship = Friend.objects.get(Q(from_user=from_user) & Q(to_user=to_user))
            if friendship.blocked:
                if friendship.status == '':
                    friendship.delete()
                else:
                    friendship.blocked = False
                    friendship.save()
        except Friend.DoesNotExist:
            raise Http404('Can not find such friend to unblock.')
