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
                'teacher',
                'teacher_categories',
                'bio',
                'image',
        ]
        widgets = {
            'categories': CheckboxSelectMultiple(),
            'teacher_categories': CheckboxSelectMultiple(),
            'gender': Select(choices=(('Male', 'Male'), ('Female', 'Female')))
        }
        labels = {
            'teacher': 'Are you a dance teacher?',
            'teacher_categories': 'Please select dances you teach'
        }

    def __init__(self, user=None, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # self.fields['user'] = Resta