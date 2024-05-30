from django import forms
from django.forms import formset_factory

from main.models import Purchases, ProductsForPurchase


class PurchaseCreateForm(forms.ModelForm):
    class Meta:
        model = Purchases
        fields = ['suppliersId', 'statusId']
        widgets = {
            'date': forms.HiddenInput(),
            'updateDate': forms.HiddenInput(),
        }

        labels = {
            'suppliersId': 'Поставщик',
            'statusId': 'Статус заказа',

        }

class PurchaseEditForm(forms.ModelForm):
    class Meta:
        model = Purchases
        fields = ['statusId']
        widgets = {
            # 'date': forms.HiddenInput(),
            'updateDate': forms.HiddenInput(),
        }

        labels = {
            'statusId': 'Статус заказа',
        }

class ProductForPurchaseForm(forms.ModelForm):
    class Meta:
        model = ProductsForPurchase
        fields = ['productId', 'quantity', 'price']

        labels = {
            'productId': 'Товар',
            'quantity': 'Количество',
            'price': 'Цена'

        }