# Create your views here.
from django.db.models import Count, Sum
from django.views.generic import ListView

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from clients.forms import ClientsForm
from main.models import Clients, Sells, Suppliers, Purchases, Products, ProductsForSell, ProductsForPurchase


# Создаем вью для отрисовки главной страницы
def home(request):
    return render(request, 'main/main.html')





class StatsListView(ListView):
    template_name = 'statistics/stats_list.html'  # Укажите ваш шаблон
    model = Clients

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Подсчет общего количества клиентов, поставщиков, заказов, закупок и товаров
        total_clients = Clients.objects.count()
        total_suppliers = Suppliers.objects.count()
        total_purchases = Purchases.objects.count()
        total_sells = Sells.objects.count()
        total_products = Products.objects.count()

        # Передача результатов подсчетов в контекст
        context['total_clients'] = total_clients
        context['total_suppliers'] = total_suppliers
        context['total_purchases'] = total_purchases
        context['total_sells'] = total_sells
        context['total_products'] = total_products

        return context



class StatsClientsListView(ListView):
    model = Clients
    template_name = 'statistics/stats_clients.html'
    context_object_name = 'clients'

    ordering = 'name'
    order_directions = {
        'name': 'asc',
        'num_sells': 'asc',
        'total_amount': 'asc'
    }

    def get_queryset(self):
        order_by = self.request.GET.get('order_by')
        direction = self.request.GET.get('direction', 'asc')

        if order_by in self.order_directions:
            if direction == 'asc':
                self.ordering = order_by
                self.order_directions[order_by] = 'desc'
            else:
                self.ordering = '-' + order_by
                self.order_directions[order_by] = 'asc'

        # Используем аннотацию для подсчета заказов и агрегацию для суммирования общей суммы
        return Clients.objects.annotate(
            num_sells=Count('sells'),
            total_amount=Sum('sells__amount_price')
        ).order_by(self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_clients'] = self.get_queryset().count()
        return context


class StatsSuppliersListView(ListView):
    model = Suppliers
    template_name = 'statistics/stats_suppliers.html'  # Замените на свой путь к шаблону
    context_object_name = 'suppliers'

    ordering = 'name'
    order_directions = {
        'name': 'asc',
        'num_purchases': 'asc',
        'total_amount': 'asc'
    }

    def get_queryset(self):
        order_by = self.request.GET.get('order_by')
        direction = self.request.GET.get('direction', 'asc')

        if order_by in self.order_directions:
            if direction == 'asc':
                self.ordering = order_by
                self.order_directions[order_by] = 'desc'
            else:
                self.ordering = '-' + order_by
                self.order_directions[order_by] = 'asc'

        # Используем аннотацию для подсчета закупок и агрегацию для суммирования общей суммы
        return Suppliers.objects.annotate(
            num_purchases=Count('purchases'),
            total_amount=Sum('purchases__amount_price')
        ).order_by(self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_suppliers'] = self.get_queryset().count()
        return context

class StatsProductsForSellListView(ListView):
    model = ProductsForSell
    template_name = 'statistics/stats_products_for_sell.html'
    context_object_name = 'products'

    ordering = 'productId__name'
    order_directions = {
        'productId__name': 'asc',
        'num_orders': 'asc',
        'total_quantity': 'asc',
        'total_amount': 'asc'  # Новое поле для сортировки
    }

    def get_queryset(self):
        order_by = self.request.GET.get('order_by')
        direction = self.request.GET.get('direction', 'asc')

        if order_by in self.order_directions:
            if direction == 'asc':
                self.ordering = order_by
                self.order_directions[order_by] = 'desc'
            else:
                self.ordering = '-' + order_by
                self.order_directions[order_by] = 'asc'

        # Используем аннотацию для подсчета заказов и агрегацию для суммирования общего количества товаров и суммы
        return ProductsForSell.objects.values('productId__name').annotate(
            num_orders=Count('sellId'),
            total_quantity=Sum('quantity'),
            total_amount=Sum('amount_price')
        ).order_by(self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_products'] = self.get_queryset().count()
        return context

class StatsProductsForPurchaseListView(ListView):
    model = ProductsForPurchase
    template_name = 'statistics/stats_products_for_purchase.html'
    context_object_name = 'products'

    ordering = 'productId__name'
    order_directions = {
        'productId__name': 'asc',
        'num_purchases': 'asc',
        'total_quantity': 'asc',
        'total_amount': 'asc'
    }

    def get_queryset(self):
        order_by = self.request.GET.get('order_by')
        direction = self.request.GET.get('direction', 'asc')

        if order_by in self.order_directions:
            if direction == 'asc':
                self.ordering = order_by
                self.order_directions[order_by] = 'desc'
            else:
                self.ordering = '-' + order_by
                self.order_directions[order_by] = 'asc'

        # Используем аннотацию для подсчета закупок и агрегацию для суммирования общего количества товаров и суммы
        return ProductsForPurchase.objects.values('productId__name').annotate(
            num_purchases=Count('purchaseId'),
            total_quantity=Sum('quantity'),
            total_amount=Sum('amount_price')
        ).order_by(self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_products'] = self.get_queryset().count()
        return context

class StatsCashListView(ListView):
    template_name = 'statistics/stats_cash.html'
    context_object_name = 'cash_stats'

    def get_queryset(self):
        total_sell_amount = ProductsForSell.objects.aggregate(total=Sum('amount_price'))['total'] or 0
        total_purchase_amount = ProductsForPurchase.objects.aggregate(total=Sum('amount_price'))['total'] or 0
        profit = total_sell_amount - total_purchase_amount

        return {
            'total_sell_amount': total_sell_amount,
            'total_purchase_amount': total_purchase_amount,
            'profit': profit,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cash_stats'] = self.get_queryset()
        return context