from django.urls import path


from django.conf import settings
from django.conf.urls.static import static

from .views import home, SuppliersListView, SuppliersDetailView, SuppliersCreateView, SuppliersUpdateView, \
    SuppliersDeleteView

#Создаем юрл пути для главного приложения



urlpatterns = [
    path('', home, name='home'),
    path('suppliers/', SuppliersListView.as_view(), name='suppliers_list'),
    path('suppliers/<int:pk>/', SuppliersDetailView.as_view(), name='suppliers_detail'),
    path('suppliers/create/', SuppliersCreateView.as_view(), name='suppliers_create'),
    path('suppliers/<int:pk>/update/', SuppliersUpdateView.as_view(), name='suppliers_update'),
    path('suppliers/<int:pk>/delete/', SuppliersDeleteView.as_view(), name='suppliers_delete'),



    # path('your-path/', views.your_view, name='your_view_url_name')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)