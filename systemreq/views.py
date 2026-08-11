from django.shortcuts import render
from django.views.generic import ListView , CreateView , UpdateView , DeleteView
from django.urls import reverse_lazy
from .models import Servey, Quisetion, AnswerOption, UserServey, UserAnswer
from .forms import ServeyForm


class ServeyListView(ListView):
    model = Servey
    template_name = 'systemreq/servey_list.html'
    context_object_name = 'serveys'

class ServeyCreateView(CreateView):
    model = Servey
    template_name = 'systemreq/servey_create.html'
    form_class = ServeyForm
    success_url = reverse_lazy('servey_list')

class ServeyUpdateView(UpdateView):
    model = Servey
    template_name = 'systemreq/servey_update.html'
    form_class = ServeyForm
    success_url = reverse_lazy('servey_list')


class ServeyDeleteView(DeleteView):
    model = Servey
    template_name = 'systemreq/servey_confirm_delete.html'
    success_url = reverse_lazy('servey_list')

