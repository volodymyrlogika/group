from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Додай дефолтне значення або дозволь нульові значення:


# Create your models here.

class Servey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    

    def __str__(self):
        return self.title

class Quisetion(models.Model):
    servey = models.ForeignKey(Servey, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    page_number = models.IntegerField(default=1)
    order = models.IntegerField(default=1)
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.text


class AnswerOption(models.Model):
    quition = models.ForeignKey(Quisetion, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)



class UserServey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    servey = models.ForeignKey(Servey, on_delete=models.CASCADE)
    result = models.FloatField(default=0.0)
    time_taken = models.DurationField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ("user", "servey")


class UserAnswer(models.Model):
    user_servey = models.ForeignKey(UserServey, related_name='answers', on_delete=models.CASCADE)
    quition = models.ForeignKey(Quisetion, on_delete=models.CASCADE)
    answer_option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ("user_servey", "quition")



