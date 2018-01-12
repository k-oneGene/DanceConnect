from django import forms
from django.forms import CheckboxSelectMultiple, Select, TextInput, RadioSelect

from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = [
                'categories',
                'name',
                'location',
                'type',
                'description',
                'start',
                'end',
                'image',
        ]
        widgets = {
            'categories': CheckboxSelectMultiple(),
            # 'start': TextInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            # 'end': TextInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        labels = {
            'name': 'Event name',
            'categories': 'Dance types',
        }

    start = forms.DateTimeField(required=True, input_formats=['%Y-%m-%dT%H:%M'], widget=TextInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    end = forms.DateTimeField(required=True, input_formats=['%Y-%m-%dT%H:%M'], widget=TextInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    # end = forms.CharField(required=True,widget=TextInput(attrs={'class': 'form-control'}))
