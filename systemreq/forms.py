from django import forms
from .models import Servey


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