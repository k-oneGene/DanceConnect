from django import forms
from django.forms import CheckboxSelectMultiple, Select

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
                'date_of_birth',
                'address',
                'gender',
                'categories',
                'bio'
        ]
        widgets = {
            'categories': CheckboxSelectMultiple(),
            'gender': Select(choices=(('Male', 'Male'), ('Female', 'Female')))
        }

    def __init__(self, user=None, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # self.fields['user'] = Resta