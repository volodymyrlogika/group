from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User  # якщо потрібно авторизувати вчителів

# =============================================
# 1. КЛАСИ
# =============================================
class Class(models.Model):
    GRADE_CHOICES = [
        (9, '9 клас'),
        (10, '10 клас'),
        (11, '11 клас'),
    ]

    class_name = models.CharField(max_length=10, unique=True, help_text="Наприклад: 9-А, 10-Б")
    grade = models.PositiveSmallIntegerField(choices=GRADE_CHOICES, verbose_name="Клас")
    letter = models.CharField(max_length=1, blank=True, help_text="Буква (А, Б, В...)")

    class Meta:
        verbose_name = "Клас"
        verbose_name_plural = "Класи"

    def __str__(self):
        return f"{self.class_name} ({self.get_grade_display()})"


# =============================================
# 2. СТУДЕНТИ
# =============================================
class Student(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="Прізвище Ім'я По-батькові")
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="students")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    birthday = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Учень"
        verbose_name_plural = "Учні"
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


# =============================================
# 3. ВЧИТЕЛІ
# =============================================
class Teacher(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="Прізвище Ім'я По-батькові")
    subject = models.CharField(max_length=100, help_text="Предмет (Математика, Українська мова...)")

    class Meta:
        verbose_name = "Вчитель"
        verbose_name_plural = "Вчителі"

    def __str__(self):
        return f"{self.full_name} — {self.subject}"


# =============================================
# 4. УРОКИ (щоденник уроків)
# =============================================
class Lesson(models.Model):
    LESSON_TYPE_CHOICES = [
        ('lecture', 'Лекція'),
        ('practice', 'Практика'),
        ('control', 'Контрольна'),
        ('lab', 'Лабораторна'),
        ('individual', 'Індивідуальне'),
        ('other', 'Інша'),
    ]

    class_field = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="lessons")
    date = models.DateField(verbose_name="Дата уроку")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name="lessons")
    subject = models.CharField(max_length=100, verbose_name="Предмет")
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES)
    topic = models.TextField(verbose_name="Тема уроку", blank=True)
    homework = models.TextField(verbose_name="Завдання на домівку", blank=True)
    notes = models.TextField(verbose_name="Примітки", blank=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['-date']
        unique_together = ('date', 'class_field')

    def __str__(self):
        return f"{self.date} — {self.subject} ({self.class_field})"


# =============================================
# 5. ОЦІНКИ
# =============================================
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="grades")
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(12)],
        verbose_name="Оцінка"
    )
    score_type = models.CharField(
        max_length=20,
        choices=[
            ('current', 'Поточна'),
            ('semester', 'Семестрова'),
            ('control', 'Контрольна'),
        ],
        default='current',
        verbose_name="Тип оцінки"
    )
    comment = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Оцінка"
        verbose_name_plural = "Оцінки"
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student} — {self.score}"


# =============================================
# 6. ПРОПУСКИ (абсентизм)
# =============================================
class Absence(models.Model):
    REASON_CHOICES = [
        ('illness', 'Хвороба'),
        ('excused', 'Поважна причина'),
        ('unexcused', 'Невиправдана'),
        ('other', 'Інше'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="absences")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="absences")
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)

    class Meta:
        verbose_name = "Пропуск"
        verbose_name_plural = "Пропуски"
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student} — {self.get_reason_display()}"


# =============================================
# 7. КРОКІ / ПЛАНИ УРОКІВ
# =============================================
class Plan(models.Model):
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="plans")
    date = models.DateField(verbose_name="Дата")
    plan_text = models.TextField(verbose_name="План уроку")

    class Meta:
        verbose_name = "План уроку"
        verbose_name_plural = "Плани уроків"
        unique_together = ('date', 'class_field')

    def __str__(self):
        return f"{self.date} — {self.class_field}"




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('gurnal.api.urls')),
]