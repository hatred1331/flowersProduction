# Create your views here.
from django.views.generic import ListView

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from suppliers.forms import SuppliersForm
from main.models import Suppliers, Purchases


# Создаем вью для отрисовки главной страницы
def home(request):
    return render(request, 'main/main.html')


def clients(request):
    return render(request, 'clients/clients_list.html')


# def suppliers(request):
#     return render(request, 'suppliers/suppliers_list.html')


def orders(request):
    return render(request, 'orders/orders_list.html')


def purchases(request):
    return render(request, 'purchases/purchases_list.html')


def statistics(request):
    return render(request, 'statistics/stats_list.html')


def products(request):
    return render(request, 'products/product_list.html')


class SuppliersListView(ListView):
    model = Suppliers
    template_name = 'suppliers/suppliers_list.html'
    context_object_name = 'suppliers'

    ordering = 'name'
    order_directions = {
        'name': 'asc',
        'organisation': 'asc'
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


class SuppliersDetailView(DetailView):
    model = Suppliers
    template_name = 'suppliers/suppliers_detail.html'
    context_object_name = 'supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier = self.get_object()
        purchases = Purchases.objects.filter(suppliersId=supplier)

        order_by = self.request.GET.get('order_by')
        direction = self.request.GET.get('direction', 'asc')

        if order_by:
            if direction == 'asc':
                purchases = purchases.order_by(order_by)
                new_direction = 'desc'
            else:
                purchases = purchases.order_by(f'-{order_by}')
                new_direction = 'asc'
        else:
            new_direction = 'asc'

        context['purchases'] = purchases
        context['order_by'] = order_by
        context['direction'] = direction
        context['new_direction'] = new_direction
        return context


class SuppliersCreateView(CreateView):
    model = Suppliers
    template_name = 'suppliers/suppliers_form.html'
    form_class = SuppliersForm
    success_url = reverse_lazy('suppliers_list')

    def form_valid(self, form):
        # Не устанавливайте id вручную
        return super().form_valid(form)


class SuppliersUpdateView(UpdateView):
    model = Suppliers
    template_name = 'suppliers/suppliers_form.html'
    form_class = SuppliersForm
    success_url = reverse_lazy('suppliers_list')

    def form_valid(self, form):
        return super().form_valid(form)


class SuppliersDeleteView(DeleteView):
    model = Suppliers
    template_name = 'suppliers/suppliers_confirm_delete.html'
    success_url = reverse_lazy('suppliers_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supplier'] = self.object  # передаем объект product в контекст
        return context


from django.shortcuts import render

# Create your views here.
