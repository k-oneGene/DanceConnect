from django import forms
from django.contrib.auth import get_user_model
from dal import autocomplete

from .hooks import hookset
from .models import Message, Thread


class UserModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return hookset.display_name(obj)


class UserModelMultipleChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return hookset.display_name(obj)


autocomplete.ModelSelect2(
    url='pinax_messages:user-autocomplete',
    attrs={
        # Set some placeholder
        'data-placeholder': 'Autocomplete ...',
        # Only trigger autocompletion after 3 characters have been typed
        'data-minimum-input-length': 3,
    },
)


class NewMessageForm(forms.ModelForm):

    subject = forms.CharField()
    to_user = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=autocomplete.ModelSelect2(
            url='pinax_messages:user-autocomplete',
            attrs={
                # Set some placeholder
                'data-placeholder': 'Enter username here...',
                # Only trigger autocompletion after 3 characters have been typed
                'data-minimum-input-length': 3,
            },
        )
    )
    content = forms.CharField(widget=forms.Textarea)
    # to_user = UserModelChoiceField(queryset=get_user_model().objects.none()) # original implementation. Maybe del.
    # threadTopics = forms.ModelChoiceField(queryset=Thread.objects.all(), widget=autocomplete.ModelSelect2(url='pinax_messages:thread-autocomplete')) # used to learn


    def __init__(self, *args, **kwargs):
            self.user = kwargs.pop("user")
            super(NewMessageForm, self).__init__(*args, **kwargs)
            self.fields["to_user"].queryset = hookset.get_user_choices(self.user)
            if self.initial.get("to_user") is not None:
                qs = self.fields["to_user"].queryset.filter(pk=self.initial["to_user"])
                self.fields["to_user"].queryset = qs

    def save(self, commit=True):
        data = self.cleaned_data
        return Message.new_message(
            self.user, [data["to_user"]], data["subject"], data["content"]
        )

    class Meta:
        model = Message
        fields = ["to_user", "subject", "content"]

    # widgets = {
    #     'to_user': autocomplete.ModelSelect2Multiple(url='country-autocomplete')
    # }


class NewMessageFormMultiple(forms.ModelForm):
    subject = forms.CharField()
    to_user = UserModelMultipleChoiceField(get_user_model().objects.none())
    content = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(NewMessageFormMultiple, self).__init__(*args, **kwargs)
        self.fields["to_user"].queryset = hookset.get_user_choices(self.user)
        if self.initial.get("to_user") is not None:
            qs = self.fields["to_user"].queryset.filter(pk__in=self.initial["to_user"])
            self.fields["to_user"].queryset = qs

    def save(self, commit=True):
        data = self.cleaned_data
        return Message.new_message(
            self.user, data["to_user"], data["subject"], data["content"]
        )

    class Meta:
        model = Message
        fields = ["to_user", "subject", "content"]


class MessageReplyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.thread = kwargs.pop("thread")
        self.user = kwargs.pop("user")
        super(MessageReplyForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        return Message.new_reply(
            self.thread, self.user, self.cleaned_data["content"]
        )

    class Meta:
        model = Message
        fields = ["content"]
