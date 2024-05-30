from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import home, PurchasesListView, PurchaseCreateView, PurchasesDetailView, ProductForPurchaseCreateView, \
    EditProductForPurchaseView, EditPurchaseView

#Создаем юрл пути для главного приложения



urlpatterns = [
    path('', home, name='home'),
    path('purchases/', PurchasesListView.as_view(), name='purchases_list'),
    path('purchases/<int:pk>/', PurchasesDetailView.as_view(), name='purchases_detail'),
    path('purchases/create/', PurchaseCreateView.as_view(), name='purchases_create'),
    path('purchases/purchases/<int:pk>/add_product/', ProductForPurchaseCreateView.as_view(), name='product_for_purchase_create'),
    path('purchases/purchases/edit_product/<int:pk>/', EditProductForPurchaseView.as_view(),name='edit_product_for_purchase'),
    path('purchases/purchases/edit_purchase/<int:pk>/', EditPurchaseView.as_view(), name='edit_purchase'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
