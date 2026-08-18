from django.urls import path
from .views import (
    ServeyListView,
    take_survey,
    survey_complete,
    survey_results_admin,
    mega__create_view,  # Імпортуємо нашу функцію
    ServeyDeleteView,
)

urlpatterns = [
    # CRUD для опитувань (використовуємо мега-функцію для створення і редагування)
    path('servey/list/', ServeyListView.as_view(), name='servey_list'),
    path('servey/create/', mega__create_view, name='servey_create'),
    path('servey/<int:survey_id>/update/', mega__create_view, name='servey_update'),
    path('servey/<int:pk>/delete/', ServeyDeleteView.as_view(), name='servey_delete'),
    
    
    # Проходження опитування
    path('servey/<int:pk>/take/<int:page_number>/', take_survey, name='take_survey'),
    path('servey/<int:pk>/take/', take_survey, name='take_survey_first_page'), # Для старту з 1 сторінки за замовчуванням
    path('servey/<int:pk>/complete/', survey_complete, name='survey_complete'),
    
    # Адмінська статистика
    path('servey/<int:pk>/results/', survey_results_admin, name='survey_results_admin'),
]