from django.db import models

class ProjectImage(models.Model):
    image = models.ImageField(upload_to='project_images/')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='images')
    

    def __str__(self):
        return self.name
    
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    project_link = models.URLField(max_length=300, blank=True, null=True)
    files = models.FileField(upload_to='project_files/', blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='projects')
    best_project = models.BooleanField(default=False)
    tehnologies = models.CharField(max_length=200, blank=True, null=True, help_text="Comma-separated list of technologies used in the project")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    