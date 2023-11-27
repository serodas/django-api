from rest_framework import serializers
from .models import MenuItem, Category, User, Cart, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'slug','title')

class MenuItemSerializer(serializers.ModelSerializer):
  category =  serializers.PrimaryKeyRelatedField(
    queryset=Category.objects.all()
  )
  # category =  CategorySerializer(read_only=True)
  class Meta:
    model = MenuItem
    fields = ('id', 'title', 'price', 'featured', 'category')
    
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email')
    
class CartSerializer(serializers.ModelSerializer):
  user =  serializers.PrimaryKeyRelatedField(
    queryset=User.objects.all(),
    default=serializers.CurrentUserDefault()
  )

  def validate(self, attrs):
    attrs['price'] = attrs['quantity'] * attrs['unit_price']
    return attrs

  class Meta:
    model = Cart
    fields = ('id', 'user','menuitem', 'quantity', 'unit_price', 'price')
    extra_kwargs = {
      'price' : {'read_only': True},
    }

class OrderItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = OrderItem
    fields = ('id', 'order', 'menuitem', 'quantity', 'price')

class OrderSerializer(serializers.ModelSerializer):
  orderitem = OrderItemSerializer(many=True, read_only=True, source='order')
  class Meta:
    model = Order
    fields = ('id', 'user', 'delivery_crew', 'status', 'total', 'date', 'orderitem')