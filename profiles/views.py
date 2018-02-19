from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from notify.signals import notify


from django.contrib.auth import authenticate, login

from .models import Profile
from events.models import Event
from .forms import ProfileForm

from friends.models import Friend


from django.http import HttpResponse, request
from django.shortcuts import render
from django.contrib import messages
from django.template import Template, Context

import pendulum

# Create your views here.


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


class ProfileListView(ListView):
    model = Profile

    def get_queryset(self):
        return Profile.objects.all().order_by('-user__date_joined')


class ProfileDetailView(DetailView):
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        profile = self.get_object()

        # notify.send(self.request.user, recipient=self.request.user, actor=self.request.user, verb='testing YEEEH.', nf_type='followed_user')

        # Pete request to me
        context['friend_to_me'] = Friend.objects.filter(Q(from_user=profile.user) & Q(to_user=self.request.user)).first()
        # I requested to this person
        context['me_to_friend'] = Friend.objects.filter(Q(to_user=profile.user) & Q(from_user=self.request.user)).first()
        return context


class MyPastEventsListView(ListView):
    model = Event
    template_name = 'profiles/my_past_events_list.html'
    paginate_by = 9

    def get_queryset(self):
        now = pendulum.now()
        return self.request.user.profile.events.all().filter(end__lt=now).order_by('-start')


class MyFutureEventsListView(ListView):
    model = Event
    template_name = 'profiles/my_future_events_list.html'
    paginate_by = 9

    def get_queryset(self):
        now = pendulum.now()
        return self.request.user.profile.events.all().filter(end__gte=now).order_by('start')


class MyNotificationsView(TemplateView):
    template_name = 'notifications/notifications_list.html'

    def get_context_data(self, **kwargs):
        context = super(MyNotificationsView, self).get_context_data(**kwargs)
        return context


class MyNotificationsBoxView(TemplateView):
    template_name = 'notifications/notifications_list_box.html'

    def get_context_data(self, **kwargs):
        context = super(MyNotificationsBoxView, self).get_context_data(**kwargs)
        return context


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
