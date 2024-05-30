from django.urls import path


from django.conf import settings
from django.conf.urls.static import static

from .views import home, OrdersListView, OrdersDetailView, OrderCreateView, ProductForSellCreateView, \
    EditProductForSellView, EditOrderView

#Создаем юрл пути для главного приложения



urlpatterns = [
    path('', home, name='home'),
    path('products/', OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:pk>/', OrdersDetailView.as_view(), name='orders_detail'),
    path('orders/create/', OrderCreateView.as_view(), name='orders_create'),
    path('sells/orders/<int:pk>/add_product/', ProductForSellCreateView.as_view(), name='product_for_sell_create'),
    path('sells/orders/edit_product/<int:pk>/', EditProductForSellView.as_view(),name='edit_product_for_sell'),
    path('sells/orders/edit_order/<int:pk>/', EditOrderView.as_view(), name='edit_order'),
    path('sells/orders/toggle_reserve/<int:pk>/', OrdersDetailView.as_view(), name='toggle_reserve'),





    # path('your-path/', views.your_view, name='your_view_url_name')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)