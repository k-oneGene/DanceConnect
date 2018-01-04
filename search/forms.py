from django import forms
from django.forms import CheckboxSelectMultiple, Select, TextInput

from crispy_forms.helper import FormHelper

from events.models import Event


class AdvanceSearchForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AdvanceSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    name = forms.CharField(required=False, widget=TextInput(attrs={'placeholder': "Event...", 'name': "q_event", 'id': "event", 'class': "form-control"}))
    date = forms.DateField(required=False)
    location = forms.CharField(required=False)

    class Meta:
        model = Event
        fields = [
            'categories',
        ]
        widgets = {
            'categories': CheckboxSelectMultiple(),
        }
