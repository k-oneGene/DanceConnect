from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect



from .models import Profile
from .forms import ProfileForm

# Create your views here.


class ProfileListView(ListView):
    model = Profile


class ProfileDetailView(DetailView):
    model = Profile


class SignUpCreateView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('profiles:list'))
        return super(SignUpCreateView, self).dispatch(request, *args, **kwargs)


class SignUpProfileCreateView(LoginRequiredMixin, CreateView):

    form_class = ProfileForm
    template_name = 'registration/signup_profile.html'
    success_url = reverse_lazy('profiles:list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        print(self.request.user)
        return super(SignUpProfileCreateView, self).form_valid(form)

