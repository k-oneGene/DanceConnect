from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import Http404

User = settings.AUTH_USER_MODEL

# Create your models here.

RELATIONSHIP_STATUSES = (('requested', 'requested'), ('friend', 'friend'), ('blocked', 'blocked'))


class Friend(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user+')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user+')
    status = models.CharField(max_length=255, choices=RELATIONSHIP_STATUSES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user.username}_to_{self.to_user.username}_{self.status}'

    """
    djinn makes request to adds peter
    """
    def friend_add(self, from_user, to_user, status='requested'):
        friendship, created = Friend.objects.get_or_create(from_user=from_user, to_user=to_user)
        if created:
            friendship.status = status
            friendship.save()
        return friendship, created

    """
    peter decides to accept djinn as friend.
    Creates relationship other way too automatically.
    (Or raise http404 error if this was called and there was no friend request)
    """
    def friend_accept(self, to_user, from_user):
        try:
            friendship = Friend.objects.get(Q(from_user=from_user) & Q(to_user=to_user))
            if friendship.status == 'requested':
                friendship.status = 'friend'
                friendship.save()
                # Add relationship other way
                self.friend_add(self, to_user, from_user, status='friend')
        except Friend.DoesNotExist:
            raise Http404('Can not find such request to accept')
        return friendship
