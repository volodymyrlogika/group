from django import forms
from .models import Servey
from .models import AnswerOption


class ServeyForm(forms.ModelForm):

  class Meta:
    model = Servey
    fields = ["title", "description"]
    widgets = {
        "title": forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введіть назву опитування",
            }
        ),
        "description": forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Опис опитування...",
            }
        ),
    }

class TakeSurveyForm(forms.Form):

  def __init__(self, *args, **kwargs):
    questions = kwargs.pop("questions", [])
    super().__init__(*args, **kwargs)

    for question in questions:
      options = AnswerOption.objects.filter(quition=question)
      choices = [(opt.id, opt.text) for opt in options]

      self.fields[f"question_{question.id}"] = forms.ChoiceField(
          label=question.text,
          choices=choices,
          widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
          required=True,
      )