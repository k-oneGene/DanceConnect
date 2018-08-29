from django import template

from pinax.messages.models import Thread

register = template.Library()


@register.filter
def unread(thread, user):
    """
    Check whether there are any unread messages for a particular thread for a user.
    """
    return bool(thread.userthread_set.filter(user=user, unread=True))


@register.filter
def unread_thread_count(user):
    """
    Return the number of Threads with unread messages for this user, useful for highlighting on an account bar for example.
    """
    return Thread.unread(user).count()


@register.simple_tag
def get_thread_image(thread, user):
    """
    Return image for chat thread
    """
    try:
        # print("debug stuff here")
        # print(thread.users.all().exclude(pk=user.pk))
        # print(thread.users.all().exclude(pk=user.pk).first().profile.image)
        return thread.users.all().exclude(pk=user.pk).first().profile.image.url
    except:
        return "/static/web_res/profile_list/Question_Mark.svg"



