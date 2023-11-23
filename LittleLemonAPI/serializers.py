from rest_framework import serializers
from .models import MenuItem, Category, User, Cart, Order, OrderItem

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
    
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email', 'groups')
    
class CartSerializer(serializers.ModelSerializer):
  user =  UserSerializer(read_only=True)
  user_id = serializers.IntegerField(write_only=True)
  menuitem =  MenuItemSerializer(read_only=True)
  menuitem_id = serializers.IntegerField(write_only=True)
  class Meta:
    model = Cart
    fields = ('id', 'user', 'user_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price')
    
class OrderSerializer(serializers.ModelSerializer):
  user =  UserSerializer(read_only=True)
  user_id = serializers.IntegerField(write_only=True)
  delivery_crew =  UserSerializer(read_only=True)
  delivery_crew_id = serializers.IntegerField(write_only=True)
  order_items = serializers.SerializerMethodField(method_name='get_order_items')
  def get_order_items(self, obj):
    order_items = OrderItem.objects.filter(order=obj)
    serialized_order_items = OrderItemSerializer(order_items, many=True)
    return serialized_order_items.data
  class Meta:
    model = Order
    fields = ('id', 'user', 'user_id', 'delivery_crew', 'delivery_crew_id', 'status', 'total', 'date')
    
class OrderItemSerializer(serializers.ModelSerializer):
  order =  OrderSerializer(read_only=True)
  order_id = serializers.IntegerField(write_only=True)
  menuitem =  MenuItemSerializer(read_only=True)
  menuitem_id = serializers.IntegerField(write_only=True)
  class Meta:
    model = OrderItem
    fields = ('id', 'order', 'order_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price')