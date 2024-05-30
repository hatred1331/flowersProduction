from django.core.checks import messages
from django.db.models import Sum
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from extra_views import CreateWithInlinesView, InlineFormSetFactory


from django.shortcuts import render, get_object_or_404, redirect
from main.models import Sells, ProductsForSell, Status, Purchases, ProductsForPurchase
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from purchases.forms import PurchaseCreateForm, ProductForPurchaseForm, PurchaseEditForm
from sells.forms import OrderCreateForm, ProductForSellForm, OrderEditForm


def home(request):
    return render(request, 'main/main.html')


def clients(request):
    return render(request, 'clients/clients_list.html')


def suppliers(request):
    return render(request, 'suppliers/suppliers_list.html')


def orders(request):
    return render(request, 'orders/orders_list.html')


# def purchases(request):
#     return render(request, 'purchases/purchases_list.html')


def statistics(request):
    return render(request, 'statistics/stats_list.html')


def products(request):
    return render(request, 'products/product_list.html')

class PurchasesListView(ListView):
    model = Purchases
    template_name = 'purchases/purchases_list.html'
    context_object_name = 'purchases'
    ordering = 'amount_price'
    order_directions = {
        'suppliersId__name': 'asc',
        'organisation': 'asc',
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


class PurchasesDetailView(DetailView):
    model = Purchases
    template_name = 'purchases/purchases_detail.html'
    context_object_name = 'purchase'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchase_id = self.kwargs['pk']

        # Получаем все продукты для заказа
        products = ProductsForPurchase.objects.filter(purchaseId__id=purchase_id)


        # Рассчитываем общую сумму для каждого товара
        for product in products:
            product.amount_price = product.quantity * product.price if product.quantity is not None and product.price is not None else None

        # Bulk update для сохранения обновлений
        ProductsForPurchase.objects.bulk_update(products, ['amount_price'])

        context['products'] = products
        for product in products:
            product.save()
        context['add_product_url'] = reverse('product_for_purchase_create', args=[purchase_id])
        return context


class PurchaseCreateView(CreateWithInlinesView):
    template_name = 'purchases/purchases_form.html'  # Укажите ваш шаблон
    form_class = PurchaseCreateForm
    product_form_class = ProductForSellForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form,})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return
        purchase_instance = form.save(commit=False)
        purchase_instance.date = purchase_instance.updateDate = timezone.now()
        purchase_instance.save()



        return redirect('purchases_list')

        return render(request, self.template_name, {'form': form})

class ProductForPurchaseCreateView(View):
    template_name = 'purchases/product_form.html'
    form_class = ProductForPurchaseForm

    def get_purchase_id(self):
        purchase_id = self.kwargs.get('pk')
        return purchase_id

    def get(self, request, *args, **kwargs):
        form = ProductForSellForm()
        context = {'product_form': form}
        context['purchase_id'] = self.get_purchase_id()

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        purchase_id = self.get_purchase_id()

        if form.is_valid() and purchase_id:
            product_instance = form.save(commit=False)
            product_instance.purchaseId_id = purchase_id
            product_instance.amount_price = product_instance.quantity * product_instance.price
            product_instance.save()

            # Обновляем общую сумму в заказе
            purchase_instance = Purchases.objects.get(id=purchase_id)
            purchase_instance.amount_price += product_instance.amount_price
            purchase_instance.save()

            return redirect('purchases_detail', pk=purchase_id)

        return render(request, self.template_name, {'form': form})


class EditProductForPurchaseView(View):
    template_name = 'purchases/edit_product_for_purchase.html'
    form_class = ProductForPurchaseForm

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs['pk']
        product = get_object_or_404(ProductsForPurchase, id=product_id)
        form = self.form_class(instance=product)
        context = {'form': form, 'product_id': product_id}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs['pk']
        product = get_object_or_404(ProductsForPurchase, id=product_id)
        form = self.form_class(request.POST, instance=product)

        if form.is_valid():
            edited_product = form.save(commit=False)
            edited_product.amount_price = edited_product.quantity * edited_product.price
            edited_product.save()

            # Обновляем общую сумму в заказе
            purchase_id = edited_product.purchaseId.id
            purchase_instance = Purchases.objects.get(id=purchase_id)
            if purchase_instance.amount_price is not None:
                purchase_instance.amount_price += edited_product.amount_price - product.amount_price
            else:
                purchase_instance.amount_price = edited_product.amount_price

            purchase_instance.save()


            return redirect('purchases_detail', pk=purchase_id)

        context = {'form': form, 'product_id': product_id}
        return render(request, self.template_name, context)

class EditPurchaseView(View):
    template_name = 'purchases/edit_purchase.html'
    form_class = PurchaseEditForm

    def get(self, request, *args, **kwargs):
        purchase_id = self.kwargs['pk']
        purchase = get_object_or_404(Purchases, id=purchase_id)
        form = self.form_class(instance=purchase)
        context = {'form': form, 'purchase_id': purchase_id}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        purchase_id = self.kwargs['pk']
        purchase = get_object_or_404(Purchases, id=purchase_id)
        form = self.form_class(request.POST, instance=purchase)

        if form.is_valid():
            form.save()
            return redirect('purchases_detail', pk=purchase_id)

        context = {'form': form, 'purchase_id': purchase_id}
        return render(request, self.template_name, context)





