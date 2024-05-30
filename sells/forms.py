from django import forms
from django.forms import formset_factory

from main.models import Sells, ProductsForSell, Products


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Sells
        fields = ['clientsId', 'statusId']
        widgets = {
            'date': forms.HiddenInput(),
            'updateDate': forms.HiddenInput(),
        }

        labels = {
            'clientsId': 'Клиент',
            'statusId': 'Статус заказа',

        }

class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Sells
        fields = ['statusId']
        widgets = {
            # 'date': forms.HiddenInput(),
            'updateDate': forms.HiddenInput(),
        }

        labels = {
            'statusId': 'Статус заказа',
        }

class ProductForSellForm(forms.ModelForm):
    class Meta:
        model = ProductsForSell
        fields = ['productId', 'quantity', 'price']

        labels = {
            'productId': 'Товар',
            'quantity': 'Количество',
            'price': 'Цена'

        }

