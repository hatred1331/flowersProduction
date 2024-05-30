from django.shortcuts import redirect
from django.urls import path


from django.conf import settings
from django.conf.urls.static import static

from stats.views import StatsListView
from .views import (home)


#Создаем юрл пути для главного приложения



urlpatterns = [
    path('', home, name='home'),
    # path('', lambda request: redirect('stats_home'), name='redirect_home'),  # Перенаправление с корневого URL на страницу со статистикой
    # path('stats_home/', StatsListView.as_view(), name='stats_home'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)