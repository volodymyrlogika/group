from django.contrib import admin
from .models import Servey, Quisetion, AnswerOption, UserServey, UserAnswer



# Register your models here.



admin.site.register(Servey)
admin.site.register(Quisetion)
admin.site.register(AnswerOption)
admin.site.register(UserServey)
admin.site.register(UserAnswer)
