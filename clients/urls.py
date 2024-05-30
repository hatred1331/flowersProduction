from django.urls import path


from django.conf import settings
from django.conf.urls.static import static

from .views import home, ClientsListView, ClientsDetailView, ClientsCreateView, ClientsUpdateView, ClientsDeleteView

#Создаем юрл пути для главного приложения



urlpatterns = [
    path('', home, name='home'),
    path('clients/', ClientsListView.as_view(), name='clients_list'),
    path('clients/<int:pk>/', ClientsDetailView.as_view(), name='clients_detail'),
    path('clients/create/', ClientsCreateView.as_view(), name='clients_create'),
    path('clients/<int:pk>/update/', ClientsUpdateView.as_view(), name='clients_update'),
    path('clients/<int:pk>/delete/', ClientsDeleteView.as_view(), name='clients_delete'),



    # path('your-path/', views.your_view, name='your_view_url_name')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)