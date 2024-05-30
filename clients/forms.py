from django import forms
from main.models import  Clients

class ClientsForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = '__all__'

        labels = {
            'name': 'Клиент',
            'phone_number': 'Номер телефона',


        }