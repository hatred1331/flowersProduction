from django.urls import path


from django.conf import settings
from django.conf.urls.static import static

from .views import home, StatsListView, StatsClientsListView, StatsSuppliersListView, StatsProductsForSellListView, \
    StatsProductsForPurchaseListView, StatsCashListView

#Создаем юрл пути для главного приложения



urlpatterns = [
    path('', home, name='home'),
    path('stats/', StatsListView.as_view(), name='stats_list'),
    path('stats/clients', StatsClientsListView.as_view(), name='stats_clients'),
    path('stats/suppliers', StatsSuppliersListView.as_view(), name='stats_suppliers'),
    path('stats/products_for_sell', StatsProductsForSellListView.as_view(), name='stats_products_for_sell'),
    path('stats/products_for_purchase', StatsProductsForPurchaseListView.as_view(), name='stats_products_for_purchase'),
    path('stats/cash', StatsCashListView.as_view(), name='stats_cash'),





] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)