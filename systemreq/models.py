from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Servey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User , on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Quisetion(models.Model):
    servey = models.ForeignKey(Servey, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    page_number = models.IntegerField(default=1)

    def __str__(self):
        return self.text


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quitions = models.ForeignKey(Quisetion, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        unique_together = ("user", "quitions")


