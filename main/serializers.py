# serializers.py

from rest_framework import serializers
from .models import ProductType, Products, Rose, Tree, Users, Clients, Suppliers, Status, Purchases, ProductsForPurchase, Sells, ProductsForSell

# Сериализатор для модели ProductType
class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'

# Сериализатор для модели Products
class ProductsSerializer(serializers.ModelSerializer):
    # Вложенный сериализатор для поля plant_type
    plant_type = ProductTypeSerializer()

    class Meta:
        model = Products
        fields = '__all__'

# Сериализатор для модели Rose
class RoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rose
        fields = '__all__'

# Сериализатор для модели Tree
class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tree
        fields = '__all__'

# Сериализатор для модели Users
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['name', 'post']

# Сериализатор для модели Clients
class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'

# Сериализатор для модели Suppliers
class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = '__all__'

# Сериализатор для модели Status
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

# Сериализатор для модели Purchases
class PurchasesSerializer(serializers.ModelSerializer):
    # Вложенные сериализаторы для полей suppliersId и statusId
    suppliersId = SuppliersSerializer()
    statusId = StatusSerializer()

    class Meta:
        model = Purchases
        fields = '__all__'

# Сериализатор для модели ProductsForPurchase
class ProductsForPurchaseSerializer(serializers.ModelSerializer):
    # Вложенные сериализаторы для полей purchaseId и productId
    purchaseId = PurchasesSerializer()
    productId = ProductsSerializer()

    class Meta:
        model = ProductsForPurchase
        fields = '__all__'

# Сериализатор для модели Sells
class SellsSerializer(serializers.ModelSerializer):
    # Вложенные сериализаторы для полей suppliersId и statusId
    suppliersId = ClientsSerializer()
    statusId = StatusSerializer()

    class Meta:
        model = Sells
        fields = '__all__'

# Сериализатор для модели ProductsForSell
class ProductsForSellSerializer(serializers.ModelSerializer):
    # Вложенные сериализаторы для полей purchaseId и productId
    purchaseId = SellsSerializer()
    productId = ProductsSerializer()

    class Meta:
        model = ProductsForSell
        fields = '__all__'