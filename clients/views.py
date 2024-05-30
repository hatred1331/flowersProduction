
# Create your views here.
from django.views.generic import ListView

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from clients.forms import ClientsForm
from main.models import Clients, Sells


# Создаем вью для отрисовки главной страницы
def home(request):
    return render(request, 'main/main.html')




class ClientsListView(ListView):
    model = Clients
    template_name = 'clients/clients_list.html'
    context_object_name = 'clients'

    ordering = 'name'
    order_directions = {
        'name': 'asc',
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

class ClientsDetailView(DetailView):
    model = Clients
    template_name = 'clients/clients_detail.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.get_object()
        orders = Sells.objects.filter(clientsId=client)

        order_by = self.request.GET.get('order_by')
        direction = self.request.GET.get('direction', 'asc')

        if order_by:
            if direction == 'asc':
                orders = orders.order_by(order_by)
                new_direction = 'desc'
            else:
                orders = orders.order_by(f'-{order_by}')
                new_direction = 'asc'
        else:
            new_direction = 'asc'

        context['orders'] = orders
        context['order_by'] = order_by
        context['direction'] = direction
        context['new_direction'] = new_direction
        return context


class ClientsCreateView(CreateView):
    model = Clients
    template_name = 'clients/clients_form.html'
    form_class = ClientsForm
    success_url = reverse_lazy('clients_list')

    def form_valid(self, form):
        # Не устанавливайте id вручную
        return super().form_valid(form)

class ClientsUpdateView(UpdateView):
    model = Clients
    template_name = 'clients/clients_form.html'
    form_class = ClientsForm
    success_url = reverse_lazy('clients_list')

    def form_valid(self, form):
        # form.instance.plant_type = form.cleaned_data['plant_type']
        return super().form_valid(form)


class ClientsDeleteView(DeleteView):
    model = Clients
    template_name = 'clients/clients_confirm_delete.html'
    success_url = reverse_lazy('clients_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = self.object  # передаем объект product в контекст
        return context
