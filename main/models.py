from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
#Создаем модель Типы растений
class ProductType(models.Model):
    type = models.CharField(max_length=40) # название типа растения

    def __str__(self):
        return f"{self.type}"
#Создаем абстрактную модель растения
class Products(models.Model):
    name = models.CharField(max_length=100) #название
    quantity = models.IntegerField() #количество
    price = models.DecimalField(max_digits=10, decimal_places=2) #цена
    variety = models.CharField(max_length=100) # сорт растения
    plant_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True) # поле тип растения, которое берется из модели Типы Растений

    def __str__(self):
        return f"{self.name}"


#Создаем дочернюю модель модели растения розы
class Rose(models.Model):
    plantId = models.ForeignKey(Products, on_delete=models.CASCADE, default=1)
    color = models.CharField(max_length=50) # цвет розы
    bud_type = models.CharField(max_length=50) # вид бутона
    rose_type = models.CharField(max_length=50) # семейство розы

    def __str__(self):
        return f"{self.rose_type}"
##Создаем дочернюю модель модели растения деревья
class Tree(models.Model):
    plantId = models.ForeignKey(Products, on_delete=models.CASCADE, default=1)
    fruits = models.CharField(max_length=50)
    family = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.family}"
#Создаем модель пользователи
class Users(models.Model):
    name = models.CharField(max_length=100) #ФИО
    post = models.CharField(max_length=50) #Должность
    password = models.CharField(max_length=20) #пароль пользователя

    def __str__(self):
        return f"{self.name} - {self.post}"
#Создаем модель покупаетелй
class Clients(models.Model):
    name = models.CharField(max_length=100) #ФИО
    phone_number = models.CharField(max_length=100) #номер телефона

    def __str__(self):
        return f"{self.name}"
#Создаем модель Поставщики, наследуемся от модели Покупатели
class Suppliers(Clients):
    organisation = models.CharField(max_length=100) # Название организации

    def __str__(self):
        return f"{self.name} - {self.organisation}"

# Создаем список статусов для документов
class Status(models.Model):
    status = models.CharField(max_length=50) # статус документа

    def __str__(self):
        return f"{self.status}"
# Создаем модель для документа закупки
class Purchases(models.Model):
    suppliersId = models.ForeignKey(Suppliers, on_delete=models.CASCADE) # Связываем модель с моделью поставщики
    statusId = models.ForeignKey(Status, on_delete=models.CASCADE) # Связываем модель с моделью статусы
    date = models.DateTimeField(auto_now_add=True) # Дата создания, ставится дата при создании
    updateDate = models.DateTimeField(auto_now=True) # Дата обновления, дата меняется при каждом обновлении документа
    amount_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    is_reserved = models.BooleanField(default=False)  # Новое поле для флага резерва


@receiver(pre_save, sender=Purchases)
def calculate_purchase_amount(sender, instance, **kwargs):
    products = ProductsForPurchase.objects.filter(purchaseId=instance)

    # Отладочный вывод
    print(f"Products: {products}")

    purchase_amount = products.aggregate(total_purchase_amount=models.Sum('amount_price'))['total_purchase_amount']

    # Отладочный вывод
    print(f"Purchase Amount: {purchase_amount}")

    instance.amount_price = purchase_amount if purchase_amount is not None else 0


# Создаем модель для хранения товаров на закупку
class ProductsForPurchase(models.Model):
    purchaseId = models.ForeignKey(Purchases, on_delete=models.CASCADE) # Связываем модель с моделью закупки
    productId = models.ForeignKey(Products, on_delete=models.CASCADE) # Связываем модель с моделью растения
    quantity = models.IntegerField(null=True) #количество
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    amount_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)

@receiver(pre_save, sender=ProductsForPurchase)
def calculate_amount_price_for_purchase(sender, instance, **kwargs):
    if instance.quantity is not None and instance.price is not None:
        instance.amount_price = instance.quantity * instance.price
    else:
        instance.amount_price = 0  # или другое значение по умолчанию
# Создаем модель для документа продажи
class Sells(models.Model):
    clientsId = models.ForeignKey(Clients, on_delete=models.CASCADE)
    statusId = models.ForeignKey(Status, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, editable=False)
    updateDate = models.DateTimeField(auto_now=True)
    amount_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    is_reserved = models.BooleanField(default=False)  # Новое поле для флага резерва


@receiver(pre_save, sender=Sells)
def calculate_order_amount(sender, instance, **kwargs):
    products = ProductsForSell.objects.filter(sellId=instance)

    # Отладочный вывод
    print(f"Products: {products}")

    order_amount = products.aggregate(total_order_amount=models.Sum('amount_price'))['total_order_amount']

    # Отладочный вывод
    print(f"Order Amount: {order_amount}")

    instance.amount_price = order_amount if order_amount is not None else 0

# Создаем модель для хранения товаров на продажу
class ProductsForSell(models.Model):
    sellId = models.ForeignKey(Sells, on_delete=models.CASCADE)
    productId = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    amount_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

@receiver(pre_save, sender=ProductsForSell)
def calculate_amount_price(sender, instance, **kwargs):
    if instance.quantity is not None and instance.price is not None:
        instance.amount_price = instance.quantity * instance.price
    else:
        instance.amount_price = None





