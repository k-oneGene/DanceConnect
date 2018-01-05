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
                'teacher',
                'categories',
                'bio',
                'image',
        ]
        widgets = {
            'categories': CheckboxSelectMultiple(),
            'gender': Select(choices=(('Male', 'Male'), ('Female', 'Female')))
        }
        labels = {
            'teacher': 'Are you a dance teacher?'
        }

    def __init__(self, user=None, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # self.fields['user'] = Resta