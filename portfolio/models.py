from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    project_link = models.URLField(max_length=300, blank=True, null=True)
    files = models.FileField(upload_to='project_files/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    best_project = models.BooleanField(default=False)
    technologies = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Comma-separated list of technologies used in the project"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Сортування: нові проєкти будуть зверху

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Повертає URL для детального перегляду проєкту"""
        return reverse('project_detail', kwargs={'pk': self.pk})

    def get_technologies_list(self):
        """Перетворює рядок технологій "Python, Django, SQLite" на список ["Python", "Django", "SQLite"]"""
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]
        return []


class ProjectImage(models.Model):
    image = models.ImageField(upload_to='project_images/')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"Image for {self.project.name}"