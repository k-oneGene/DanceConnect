from django import forms
from django.forms import SelectMultiple, CheckboxSelectMultiple

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
                'date_of_birth',
                'address',
                'categories',
                'bio'
        ]
        widgets = {
            'categories': CheckboxSelectMultiple()
        }

