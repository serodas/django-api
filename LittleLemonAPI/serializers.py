from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'slug')

class MenuItemSerializer(serializers.ModelSerializer):
  category =  CategorySerializer(read_only=True)
  category_id = serializers.IntegerField(write_only=True)
  class Meta:
    model = MenuItem
    fields = ('id', 'title', 'price', 'featured', 'category', 'category_id')