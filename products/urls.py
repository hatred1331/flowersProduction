from django.urls import path


from django.conf import settings
from django.conf.urls.static import static

from .views import  home, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView

#Создаем юрл пути для главного приложения



urlpatterns = [
    path('', home, name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),



    # path('your-path/', views.your_view, name='your_view_url_name')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)