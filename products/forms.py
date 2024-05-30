from django import forms
from main.models import  Products

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'

        labels = {
            'name': 'Наименование',
            'quantity': 'Количество',
            'price': 'Цена',
            'variety': 'Описание',
            'plant_type': 'Тип'

        }