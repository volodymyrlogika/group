from django.contrib import admin
from .models import Project, ProjectImage


# 1. Inline-модель для зручного додавання декількох фотографій безпосередньо у формі проєкту
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3  # Кількість порожніх слотів для фото за замовчуванням
    fields = ('image',)


# 2. Основна конфігурація проєкту в адмін-панелі
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # Поля, які будуть відображатися у списку проєктів
    list_display = (
        'name',
        'author',
        'technologies',
        'best_project',
        'created_at',
    )

    # Фільтри у правому боковому меню
    list_filter = (
        'best_project',
        'created_at',
        'author',
    )

    # Поля, за якими працюватиме пошуковий рядок
    search_fields = (
        'name',
        'description',
        'technologies',
    )

    # Автоматичне встановлення поточного користувача автором під час створення через адмінку
    def save_model(self, request, obj, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, change)

    # Підключаємо галерею зображень як inline-блок
    inlines = [ProjectImageInline]