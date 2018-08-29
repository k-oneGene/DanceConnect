from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from events.models import Event
from profiles.models import Profile
from .forms import AdvanceSearchForm

# Create your views here.


class SearchHomeView(TemplateView):
    template_name = 'search/search_home.html'

    def get_context_data(self, **kwargs):
        context = super(SearchHomeView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        qs = Event.objects.all().order_by('-start')



class SearchEventsListview(ListView):
    model = Event
    template_name = 'search/searchevents_list.html'
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        context = super(SearchEventsListview, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        qs = self.get_queryset()
        if query:
            qs = Event.objects.search(query).order_by('-start')
        # context['object_list'] = qs

        paginator = Paginator(qs, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['object_list'] = page_obj
        context['paginator'] = paginator
        context['page_obj'] = page_obj

        return context

    def get_queryset(self):
        return Event.objects.filter(type__exact='event').order_by('-start')


class AdvanceSearchEventsListView(ListView):
    model = Event
    template_name = 'search/advance_searchevents_list.html'
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        context = super(AdvanceSearchEventsListView, self).get_context_data(*args, **kwargs)
        context['form'] = AdvanceSearchForm

        q_event = self.request.GET.get('q_event')
        q_date = self.request.GET.get('q_date')
        q_location = self.request.GET.get('q_location')
        categories = self.request.GET.getlist('categories')
        qs = self.get_queryset()

        #todo: Entry.objects.filter(pub_date__date__gt=datetime.date(2005, 1, 1)) <= Something like that in future
        if categories:
            qs = qs.filter(
                (Q(name__icontains=q_event) |
                Q(description__icontains=q_event)) &
                Q(start__icontains=q_date) &
                Q(categories__id__in=categories)
            ).distinct().order_by('-start')
        # for cases where Category wasn't selected. Then It's like we select everything or in query term we don't filter category
        elif q_event or q_date or q_location:
            qs = qs.filter(
                (Q(name__icontains=q_event) |
                Q(description__icontains=q_event)) &
                Q(start__icontains=q_date)
            ).distinct().order_by('-start')
        paginator = Paginator(qs, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['object_list'] = page_obj
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        context['categories_q'] = categories
        return context

    def get_queryset(self):
        return Event.objects.filter(type='event').order_by('-start')


class SearchFestivalsListView(ListView):
    model = Event
    template_name = 'search/searchfestivals_list.html'
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        context = super(SearchFestivalsListView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        qs = self.get_queryset()
        if query:
            qs = Event.objects.search(query).order_by('-start')
        # context['object_list'] = qs

        paginator = Paginator(qs, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['object_list'] = page_obj
        context['paginator'] = paginator
        context['page_obj'] = page_obj

        return context

    def get_queryset(self):
        return Event.objects.filter(type__exact='festival').order_by('-start')


class AdvanceSearchFestivalsListView(ListView):
    model = Event
    template_name = 'search/advance_searchfestivals_list.html'
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        context = super(AdvanceSearchFestivalsListView, self).get_context_data(*args, **kwargs)
        context['form'] = AdvanceSearchForm

        q_event = self.request.GET.get('q_event')
        q_date = self.request.GET.get('q_date')
        q_location = self.request.GET.get('q_location')
        categories = self.request.GET.getlist('categories')
        qs = self.get_queryset()

        #todo: Entry.objects.filter(pub_date__date__gt=datetime.date(2005, 1, 1)) <= Something like that in future
        if categories:
            qs = qs.filter(
                (Q(name__icontains=q_event) |
                 Q(description__icontains=q_event)) &
                Q(start__icontains=q_date) &
                Q(categories__id__in=categories)
            ).distinct().order_by('-start')
        # for cases where Category wasn't selected. Then It's like we select everything or in query term we don't filter category
        elif q_event or q_date or q_location:
            qs = qs.filter(
                (Q(name__icontains=q_event) |
                 Q(description__icontains=q_event)) &
                Q(start__icontains=q_date)
            ).distinct().order_by('-start')
        paginator = Paginator(qs, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['object_list'] = page_obj
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        context['categories_q'] = categories
        return context

    def get_queryset(self):
        return Event.objects.filter(type='festival').order_by('-start')


class SearchProfilesListview(ListView):
    model = Profile
    template_name = 'search/searchprofiles_list.html'
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProfilesListview, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        # qs = context['object_list'] # Profile.objects.all(), but ListView auto does this.
        qs = Profile.objects.all() # Profile.objects.all(), but ListView auto does this.
        if query:
            qs = qs.search(query)
        context['object_list'] = qs

        paginator = Paginator(qs, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['object_list'] = page_obj
        context['paginator'] = paginator
        context['page_obj'] = page_obj

        return context

class SearchTeachersListview(ListView):
    model = Profile
    template_name = 'search/searchteachers_list.html'
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        context = super(SearchTeachersListview, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        qs = Profile.objects.filter(teacher=True) # Profile.objects.all(), but ListView auto does this.
        if query:
            qs = qs.search(query)
        context['object_list'] = qs

        paginator = Paginator(qs, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['object_list'] = page_obj
        context['paginator'] = paginator
        context['page_obj'] = page_obj

        return context

