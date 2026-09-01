from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import CheckboxInput
from .models import Project, ProjectImage


class MultipleFileInput(forms.ClearableFileInput):
    """Віджет для підтримки мультизавантаження файлів у Django."""
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        default_attrs = {'multiple': True}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return files.get(name)


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ProjectForm(forms.ModelForm):
    best_project = forms.BooleanField(
        required=False,
        label='Best Project',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    images = forms.FileField(
        widget=MultipleFileInput(attrs={'class': 'form-control'}),
        required=False,
        label='Картинки проєкту (можна обрати кілька)'
    )

    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'project_link',
            'files',
            'best_project',
            'technologies',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'images':
                continue
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'