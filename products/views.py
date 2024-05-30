from django.views.generic import ListView

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView


from main.models import ProductType, Products
from products.forms import ProductsForm


# Создаем вью для отрисовки главной страницы
def home(request):
    return render(request, 'main/main.html')


def clients(request):
    return render(request, 'clients/clients_list.html')


def suppliers(request):
    return render(request, 'suppliers/suppliers_list.html')


def orders(request):
    return render(request, 'orders/orders_list.html')


def purchases(request):
    return render(request, 'purchases/purchases_list.html')


def statistics(request):
    return render(request, 'statistics/stats_list.html')




# class ProductListView(ListView):
#     model = Products
#     template_name = 'products/product_list.html'
#     context_object_name = 'products'

# class ProductListView(ListView):
#     model = Products
#     template_name = 'products/product_list.html'
#     context_object_name = 'products'
#     ordering = ['name']
#
#     def get_queryset(self):
#         order_by = self.request.GET.get('order_by', 'name')
#         if not hasattr(Products, order_by):
#             order_by = 'name'
#         return Products.objects.all().order_by(order_by)
class ProductListView(ListView):
    model = Products
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    ordering = 'name'
    order_directions = {
        'name': 'asc',
        'quantity': 'asc',
        'price': 'asc',  # Имя связанного поля статуса
        'plant_type__type': 'asc',

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

class ProductDetailView(DetailView):
    model = Products
    template_name = 'products/product_detail.html'
    context_object_name = 'product'



class ProductCreateView(CreateView):
    model = Products
    template_name = 'products/product_form.html'
    form_class = ProductsForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        # Не устанавливайте id вручную
        return super().form_valid(form)

class ProductUpdateView(UpdateView):
    model = Products
    template_name = 'products/product_form.html'
    form_class = ProductsForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.plant_type = form.cleaned_data['plant_type']
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Products
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object  # передаем объект product в контекст
        return context





