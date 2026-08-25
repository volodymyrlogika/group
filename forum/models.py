from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Thread(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва гілки")
    description = models.TextField(blank=True, verbose_name="Опис гілки")
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    views_count = models.PositiveIntegerField(default=0, verbose_name="Кількість переглядів")

    def __str__(self):
        return self.title

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(verbose_name="Текст повідомлення")
    image = models.ImageField(upload_to="forum_photos/", blank=True, null=True, verbose_name="Фото")
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    dislikes = models.ManyToManyField(User, related_name='forum_dislikes', blank=True)
    views_count = models.PositiveIntegerField(default=0, verbose_name="Кількість переглядів")

    def total_likes(self):
        return self.likes.count()
    
    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return f"Повідомлення від {self.author.username}"
