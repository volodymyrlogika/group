
#базові класи
from django.views.generic import ListView , CreateView , UpdateView , DeleteView
from django.db import transaction
#urls

from django.urls import reverse_lazy

#форми та моделі

from .forms import  TakeSurveyForm
from .models import AnswerOption, Quisetion, Servey, UserAnswer, UserServey

#шорткати
from django.shortcuts import get_object_or_404, redirect, render

#міксини
from .mixins import StaffRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from functools import wraps

def prevent_multiple_submission(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        survey_id = kwargs.get('pk') or kwargs.get('survey_id')
        
        if survey_id and request.user.is_authenticated:
            survey = get_object_or_404(Servey, pk=survey_id)
            
            # Шукаємо вже створений UserServey для цього юзера
            user_servey = UserServey.objects.filter(user=request.user, servey=survey).first()
            
            if user_servey:
                # Перевіряємо, чи опитування вже завершене (наприклад, результат > 0 або є прапорець завершення, 
                # або просто якщо юзер намагається зайти на першу сторінку GET-запитом, а воно вже є).
                # Але якщо це POST (сабміт форми) або не перша сторінка — пускаємо далі.
                page_number = kwargs.get('page_number', 1)
                if request.method == 'GET' and page_number == 1:
                    # Перевіряємо, чи є вже відповіді (тобто опитування вже пройдене до кінця)
                    if user_servey.answers.exists():
                        messages.warning(request, "Ти вже пройшов це опитування!")
                        return redirect('survey_complete', pk=survey.id)
                
        return view_func(request, *args, **kwargs)
    return _wrapped_view


class ServeyListView(LoginRequiredMixin , ListView):
    model = Servey
    template_name = 'systemreq/servey_list.html'
    context_object_name = 'serveys'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Отримуємо ID опитувань, які поточний юзер уже пройшов
        if self.request.user.is_authenticated:
            context['user_completed_surveys_ids'] = list(
                UserServey.objects.filter(user=self.request.user).values_list('servey_id', flat=True)
            )
        else:
            context['user_completed_surveys_ids'] = []
        return context


class ServeyDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Servey
    template_name = 'systemreq/servey_confirm_delete.html'
    success_url = reverse_lazy('servey_list')

def mega__create_view(request, survey_id=None):
    survey = get_object_or_404(Servey, pk=survey_id) if survey_id else None

    if request.method == "POST":
        servay_name = request.POST.get("servay_name")
        servay_description = request.POST.get("servay_description")

        with transaction.atomic():
            if survey:
                survey.title = servay_name
                survey.description = servay_description
                survey.save()
                # При повному оновленні можемо очистити старі питання
                survey.quisetion_set.all().delete()
            else:
                survey = Servey.objects.create(
                    title=servay_name,
                    description=servay_description,
                    author=request.user
                )

            # Отримуємо списки питань
            quetions_texts = request.POST.getlist("quetions_text[]")
            quetions_page_numbers = request.POST.getlist("quetions_page_number[]")
            quetions_orders = request.POST.getlist("quetions_order[]")
            quetions_images = request.FILES.getlist("quetions_image[]")

            # Проходимося по кожному питанню
            for i in range(len(quetions_texts)):
                q_text = quetions_texts[i]
                if not q_text.strip():
                    continue
                
                q_page = quetions_page_numbers[i] if i < len(quetions_page_numbers) else 1
                q_order = quetions_orders[i] if i < len(quetions_orders) else 1
                q_image = quetions_images[i] if i < len(quetions_images) else None

                question = Quisetion.objects.create(
                    servey=survey,
                    text=q_text,
                    page_number=q_page,
                    order=q_order,
                    image=q_image
                )

                # ДЛЯ КОЖНОГО ПИТАННЯ збираємо його власні варіанти відповідей через префікс або індекс у назві інпуту
                # Наприклад, у формі назва полів буде answer_text_{i}[] та answer_is_correct_{i}[]
                ans_texts = request.POST.getlist(f"answer_text_{i}[]")
                ans_corrects = request.POST.getlist(f"answer_is_correct_{i}[]")

                for j in range(len(ans_texts)):
                    a_text = ans_texts[j]
                    if not a_text.strip():
                        continue
                    
                    # Перевіряємо, чи цей індекс відповіді відзначений як правильний
                    is_corr = str(j) in ans_corrects
                    
                    AnswerOption.objects.create(
                        quition=question,
                        text=a_text,
                        is_correct=is_corr
                    )

        return redirect('servey_list')

    context = {
        'survey': survey,
    }
    return render(request, 'systemreq/mega_form.html', context)



@login_required
@prevent_multiple_submission
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
                    opt = AnswerOption.objects.get(id=int(opt_id), quition=question)
                    UserAnswer.objects.update_or_create(
                        user_servey=user_servey,
                        quition=question,
                        defaults={"answer_option": opt},
                    )

            next_page = page_number + 1
            if Quisetion.objects.filter(servey=servey, page_number=next_page).exists():
                return redirect("take_survey", pk=servey.pk, page_number=next_page)
            
            # === РАХУЄМО БАЛИ ЯК ВІДСОТОК ВІД 10 ===
            # Загальна кількість питань у всьому опитуванні
            total_questions = Quisetion.objects.filter(servey=servey).count()
            
            if total_questions > 0:
                # Рахуємо, скільки правильних відповідей дав юзер
                correct_answers = sum(
                    1 for answer in user_servey.answers.all() 
                    if answer.answer_option.is_correct
                )
                # Вираховуємо пропорцію до 10 балів
                user_servey.result = round((correct_answers / total_questions) * 10, 2)
            else:
                user_servey.result = 0.0
                
            user_servey.save()
            # ======================================

            return redirect("survey_complete", pk=servey.pk)
        else:
            print("ПОМИЛКИ ВАЛІДАЦІЇ ФОРМИ:", form.errors)
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
      "systemreq/admin_results.html",
      {"servey": servey, "user_serveys": user_serveys},
  )