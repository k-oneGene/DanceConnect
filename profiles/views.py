from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login

from .models import Profile
from .forms import ProfileForm


from django.http import HttpResponse, request
from django.shortcuts import render
from django.contrib import messages
from django.template import Template, Context

# Create your views here.


class ProfileListView(ListView):
    model = Profile

    def get_queryset(self):
        return Profile.objects.all().order_by('-user__date_joined')


class SignUpCreateView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('profiles:profile')
    template_name = 'registration/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('profiles:list'))
        return super(SignUpCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        valid = super(SignUpCreateView, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password1 = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password1)
        login(self.request, user)
        return valid


class SignUpProfileCreateView(LoginRequiredMixin, CreateView):
    form_class = ProfileForm
    template_name = 'registration/signup_profile.html'
    success_url = reverse_lazy('profiles:list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super(SignUpProfileCreateView, self).form_valid(form)


class ProfileUpdateView(UpdateView):
    model = Profile
    # fields = ['date_of_birth', 'gender', 'address', 'categories', 'bio']
    form_class = ProfileForm
    template_name = 'profiles/profile_edit.html'
    # success_url =

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('profiles:detail', kwargs={'pk': self.request.user.profile.id})


class ProfileDetailView(DetailView):
    model = Profile


def login_test_view(request):
    # user = authenticate(username='test20', password='qwerty123')
    # print(user)
    # login(request, user)
    my_html = """
    <html>
        <body>
            <h1 class='text-center'>Messages testing</h1>
            {% if messages %}
                <ul class="messages">
                {% for message in messages %}
                    <li class="{{ message.tags }}">{{ message }}</li>
                {% endfor %}
                </ul>
            {% endif %} 
        </body>
    </html>
    """
    messages.error(request, 'Please correct the error below.')
    messages.add_message(request, messages.INFO, 'Hello world.')

    messages.debug(request, '%s SQL statements were executed.' % 55)
    messages.info(request, 'Three credits remain in your account.')
    messages.success(request, 'Profile details updated.')
    messages.warning(request, 'Your account expires in three days.')
    messages.error(request, 'Document deleted.')

    context = Context({'message': messages})

    # return render(request, template_name='profiles/x_testing.html', context={})

    # print(Template(my_html).render(context=Context({'hi':'hi'})))
    # return HttpResponse(Template(my_html).render(context=Context({'hi':'hi'})))
