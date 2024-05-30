from django.core.checks import messages
from django.db.models import Sum
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from extra_views import CreateWithInlinesView, InlineFormSetFactory

from django.shortcuts import render, get_object_or_404, redirect
from main.models import Sells, ProductsForSell, Status
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from sells.forms import OrderCreateForm, ProductForSellForm, OrderEditForm


def home(request):
    return render(request, 'main/main.html')


def clients(request):
    return render(request, 'clients/clients_list.html')


def suppliers(request):
    return render(request, 'suppliers/suppliers_list.html')


# def orders(request):
#     return render(request, 'orders/orders_list.html')


def purchases(request):
    return render(request, 'purchases/purchases_list.html')


def statistics(request):
    return render(request, 'statistics/stats_list.html')


def products(request):
    return render(request, 'products/product_list.html')


class OrdersListView(ListView):
    model = Sells
    template_name = 'orders/orders_list.html'
    context_object_name = 'orders'
    ordering = 'amount_price'
    order_directions = {
        'clientsId__name': 'asc',
        'amount_price': 'asc',
        'statusId__status': 'asc',  # Имя связанного поля статуса
        'date': 'asc',
        'updateDate': 'asc',
    }

    def get_queryset(self):
        order_by = self.request.GET.get('order_by')
        if order_by in self.order_directions:
            direction = self.order_directions[order_by]
            if direction == 'asc':
                self.ordering = order_by
                self.order_directions[order_by] = 'desc'
            else:
                self.ordering = '-' + order_by
                self.order_directions[order_by] = 'asc'
        return super().get_queryset().order_by(self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_directions'] = self.order_directions
        return context

class OrdersDetailView(DetailView):
    model = Sells
    template_name = 'orders/orders_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['pk']

        # Получаем все продукты для заказа
        products = ProductsForSell.objects.filter(sellId__id=order_id)


        # Рассчитываем общую сумму для каждого товара
        for product in products:
            product.amount_price = product.quantity * product.price if product.quantity is not None and product.price is not None else None

        # Bulk update для сохранения обновлений
        ProductsForSell.objects.bulk_update(products, ['amount_price'])

        context['products'] = products
        for product in products:
            product.save()
        context['add_product_url'] = reverse('product_for_sell_create', args=[order_id])
        return context

    # def post(self, request, *args, **kwargs):
    #     order_id = kwargs['pk']
    #
    #     try:
    #         sells = Sells.objects.get(id=order_id)
    #         products_for_sell = ProductsForSell.objects.filter(sellId__id=order_id)
    #     except (Sells.DoesNotExist, ProductsForSell.DoesNotExist):
    #         return self.render_to_response(self.get_context_data())
    #
    #     # Инвертируем статус резерва для заказа
    #     sells.is_reserved = not sells.is_reserved
    #
    #     if sells.is_reserved:
    #         # Создаем резерв
    #         for product_for_sell in products_for_sell:
    #             product = product_for_sell.productId
    #             product.quantity -= product_for_sell.quantity
    #             product_for_sell.is_reserved = True
    #             product_for_sell.save()
    #             product.save()
    #     else:
    #         # Отменяем резерв и возвращаем товары в таблицу Products
    #         for product_for_sell in products_for_sell:
    #             product = product_for_sell.productId
    #             product.quantity += product_for_sell.quantity
    #             product_for_sell.is_reserved = False
    #             product_for_sell.save()
    #             product.save()
    #
    #     sells.save()
    #
    #     return self.render_to_response(self.get_context_data())





# Устанавливаем pip install django-extra-views
class OrderCreateView(CreateWithInlinesView):
    template_name = 'orders/orders_form.html'  # Укажите ваш шаблон
    form_class = OrderCreateForm
    product_form_class = ProductForSellForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form,})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return
        sell_instance = form.save(commit=False)
        sell_instance.date = sell_instance.updateDate = timezone.now()
        sell_instance.save()



        return redirect('orders_list')

        return render(request, self.template_name, {'form': form})


class ProductForSellCreateView(View):
    template_name = 'orders/product_form.html'
    form_class = ProductForSellForm

    def get_sell_id(self):
        sell_id = self.kwargs.get('pk')
        return sell_id

    def get(self, request, *args, **kwargs):
        form = ProductForSellForm()
        context = {'product_form': form}
        context['sell_id'] = self.get_sell_id()

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        sell_id = self.get_sell_id()

        if form.is_valid() and sell_id:
            product_instance = form.save(commit=False)
            product_instance.sellId_id = sell_id
            product_instance.amount_price = product_instance.quantity * product_instance.price
            product_instance.save()

            # Обновляем общую сумму в заказе
            sell_instance = Sells.objects.get(id=sell_id)
            sell_instance.amount_price += product_instance.amount_price
            sell_instance.save()

            return redirect('orders_detail', pk=sell_id)

        return render(request, self.template_name, {'form': form})


class EditProductForSellView(View):
    template_name = 'orders/edit_product_for_sell.html'
    form_class = ProductForSellForm

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs['pk']
        product = get_object_or_404(ProductsForSell, id=product_id)
        form = self.form_class(instance=product)
        context = {'form': form, 'product_id': product_id}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs['pk']
        product = get_object_or_404(ProductsForSell, id=product_id)
        form = self.form_class(request.POST, instance=product)

        if form.is_valid():
            edited_product = form.save(commit=False)
            edited_product.amount_price = edited_product.quantity * edited_product.price
            edited_product.save()

            # Обновляем общую сумму в заказе
            sell_id = edited_product.sellId.id
            sell_instance = Sells.objects.get(id=sell_id)
            sell_instance.amount_price += edited_product.amount_price - product.amount_price
            sell_instance.save()

            return redirect('orders_detail', pk=sell_id)

        context = {'form': form, 'product_id': product_id}
        return render(request, self.template_name, context)

class EditOrderView(View):
    template_name = 'orders/edit_order.html'
    form_class = OrderEditForm

    def get(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order = get_object_or_404(Sells, id=order_id)
        form = self.form_class(instance=order)
        context = {'form': form, 'order_id': order_id}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order = get_object_or_404(Sells, id=order_id)
        form = self.form_class(request.POST, instance=order)

        if form.is_valid():
            form.save()
            return redirect('orders_detail', pk=order_id)

        context = {'form': form, 'order_id': order_id}
        return render(request, self.template_name, context)






