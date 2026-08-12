
#базові класи
from django.views.generic import ListView , CreateView , UpdateView , DeleteView

#urls

from django.urls import reverse_lazy

#форми та моделі

from .forms import ServeyForm, TakeSurveyForm
from .models import AnswerOption, Quisetion, Servey, UserAnswer, UserServey

#шорткати
from django.shortcuts import get_object_or_404, redirect, render

#міксини
from .mixins import StaffRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test




class ServeyListView(LoginRequiredMixin , ListView):
    model = Servey
    template_name = 'systemreq/servey_list.html'
    context_object_name = 'serveys'

class ServeyCreateView(LoginRequiredMixin , StaffRequiredMixin , CreateView):
    model = Servey
    template_name = 'systemreq/servey_create.html'
    form_class = ServeyForm
    success_url = reverse_lazy('servey_list')

class ServeyUpdateView(LoginRequiredMixin , StaffRequiredMixin , UpdateView):
    model = Servey
    template_name = 'systemreq/servey_update.html'
    form_class = ServeyForm
    success_url = reverse_lazy('servey_list')


class ServeyDeleteView(LoginRequiredMixin , StaffRequiredMixin , DeleteView):
    model = Servey
    template_name = 'systemreq/servey_confirm_delete.html'
    success_url = reverse_lazy('servey_list')

@login_required
def take_survey(request, pk, page_number=1):
  servey = get_object_or_404(Servey, pk=pk)
  user_servey, _ = UserServey.objects.get_or_create(
      user=request.user, servey=servey
  )
  questions = Quisetion.objects.filter(
      servey=servey, page_number=page_number
  ).order_by("order")

  if not questions.exists():
    return redirect("survey_complete", pk=servey.pk)

  if request.method == "POST":
    form = TakeSurveyForm(request.POST, questions=questions)
    if form.is_valid():
      for question in questions:
        opt_id = form.cleaned_data.get(f"question_{question.id}")
        if opt_id:
          opt = AnswerOption.objects.get(id=opt_id, quition=question)
          UserAnswer.objects.update_or_create(
              user_servey=user_servey,
              quition=question,
              defaults={"answer_option": opt},
          )

      next_page = page_number + 1
      if Quisetion.objects.filter(servey=servey, page_number=next_page).exists():
        return redirect("take_survey", pk=servey.pk, page_number=next_page)
      return redirect("survey_complete", pk=servey.pk)
  else:
    form = TakeSurveyForm(questions=questions)

  return render(
      request,
      "systemreq/take_survey.html",
      {"servey": servey, "form": form, "page_number": page_number},
  )

@login_required
def survey_complete(request, pk):
    survay = get_object_or_404(Servey, pk=pk)
    user_servey = get_object_or_404(UserServey, user=request.user, servey=survay)
    return render(request, "systemreq/survey_complete.html", {"servey": survay, "user_servey": user_servey})

def is_staff_check(user):
  return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
@user_passes_test(is_staff_check, login_url='no_permission')
def survey_results_admin(request, pk):
  servey = get_object_or_404(Servey, pk=pk)
  user_serveys = UserServey.objects.filter(servey=servey)
  return render(
      request,
      "systemreq/survey_results_admin.html",
      {"servey": servey, "user_serveys": user_serveys},
  )