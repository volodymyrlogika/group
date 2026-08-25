from django import forms
from .models import AnswerOption, Quisetion

class TakeSurveyForm(forms.Form):

    def __init__(self, *args, **kwargs):
        questions = kwargs.pop("questions", [])
        super().__init__(*args, **kwargs)

        for question in questions:
            options = AnswerOption.objects.filter(quition=question)
            choices = [(opt.id, opt.text) for opt in options]

            field_name = f"question_{question.id}"
            self.fields[field_name] = forms.ChoiceField(
                label=question.text,
                choices=choices,
                widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
                required=True,
            )
            # Прив'язуємо об'єкт питання прямо до поля форми!
            self.fields[field_name].question = question