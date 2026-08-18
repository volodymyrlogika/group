from django import forms
from .models import Project, ProjectImage
from django.forms import CheckboxInput
class ProjectForm(forms.ModelForm):
    best_project = forms.BooleanField(required=False, label='Best Project', widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    class Meta:
        model = Project
        fields = ['name', 'description', 'project_link', 'files', 'best_project', 'technologies']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'