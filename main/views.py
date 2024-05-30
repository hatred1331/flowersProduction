from django.views.generic import ListView

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from rest_framework import generics
from rest_framework.generics import ListAPIView

from .models import ProductType, Products
from .serializers import ProductTypeSerializer, ProductsSerializer


#Создаем вью для отрисовки главной страницы
def home(request):
    return render(request, 'statistics/stats_list.html')















