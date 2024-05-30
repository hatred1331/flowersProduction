from django import forms
from main.models import  Suppliers

class SuppliersForm(forms.ModelForm):
    class Meta:
        model = Suppliers
        fields = '__all__'

        labels = {
            'name': 'Клиент',
            'phone_number': 'Номер телефона',
            'organisation': 'Организация'
        }