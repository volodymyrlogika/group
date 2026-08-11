import calendar
from collections import defaultdict
from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .forms import EventForm
from .models import Event


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return redirect('home')


class HomeView(ListView):
    model = Event
    template_name = 'main/home.html'
    context_object_name = 'upcoming_events'

    def get_queryset(self):
        return Event.objects.filter(start_time__gte=timezone.now()).order_by('start_time')[:6]


class EventListView(ListView):
    model = Event
    template_name = 'main/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.order_by('start_time')


class EventDetailView(DetailView):
    model = Event
    template_name = 'main/event_detail.html'
    context_object_name = 'event'


class EventCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'main/event_form.html'
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'main/event_form.html'
    success_url = reverse_lazy('event_list')


class EventDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Event
    template_name = 'main/event_confirm_delete.html'
    success_url = reverse_lazy('event_list')


class EventCalendarView(TemplateView):
    template_name = 'main/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localtime(timezone.now())
        year = int(self.request.GET.get('year', today.year))
        month = int(self.request.GET.get('month', today.month))

        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdatescalendar(year, month)

        events = Event.objects.filter(
            start_time__year=year,
            start_time__month=month,
        )

        events_by_date = defaultdict(list)
        for event in events:
            events_by_date[event.start_time.date()].append(event)

        month_weeks = []
        for week in month_days:
            week_days = []
            for day in week:
                week_days.append({
                    'date': day,
                    'events': events_by_date.get(day, []),
                })
            month_weeks.append(week_days)

        context.update({
            'year': year,
            'month': month,
            'month_name': calendar.month_name[month],
            'weekdays': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд'],
            'month_weeks': month_weeks,
            'prev_month': (datetime(year, month, 1) - timedelta(days=1)).strftime('%Y-%m'),
            'next_month': (datetime(year, month, 28) + timedelta(days=7)).strftime('%Y-%m'),
        })
        return context
