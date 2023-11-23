from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from .models import MenuItem, Category, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CategorySerializer, UserSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage

@permission_classes([IsAdminUser])
class CategoriesView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def menu_items(request):
  if request.method == 'GET':
    items = MenuItem.objects.select_related('category').all()
    
    search =  request.query_params.get('search')
    ordering = request.query_params.get('ordering')
    perpage = request.query_params.get('perpage', default=1)
    page = request.query_params.get('page', default=1)
    
    title = request.query_params.get('title')
    price = request.query_params.get('price')
    featured = request.query_params.get('featured')
    category_slug = request.query_params.get('category')
    if title:
      items = items.filter(title=title)
    if price:
      items = items.filter(price=price)
    if featured:
      items = items.filter(featured=featured)
    if category_slug:
      items = items.filter(category__slug=category_slug)
    if search:
      items = items.filter(title__contains=search)
    if ordering:
      ordering_fields = ordering.split(",")
      items = items.order_by(*ordering_fields)
    else:
      items = items.order_by('id')

    paginator = Paginator(items, per_page = perpage)
    try :
      items = paginator.page(number = page)
    except EmptyPage:
      items = []
    serialized_items = MenuItemSerializer(items, many=True)
    return Response(serialized_items.data)
  if request.method == 'POST':
    if request.user.groups.filter(name='Manager').exists():
      serialized_item = MenuItemSerializer(data=request.data)
      serialized_item.is_valid(raise_exception=True)
      serialized_item.save()
      return Response(serialized_item.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@permission_classes([IsAuthenticated])
def menu_item(request, pk):
  if request.method == 'GET':
    item = get_object_or_404(MenuItem, pk=pk)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)
  else:
    if request.user.groups.filter(name='Manager').exists():
      item = get_object_or_404(MenuItem, pk=pk)
      if request.method == 'PUT':
        serialized_item = MenuItemSerializer(item, data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data)
      elif request.method == 'PATCH':
        serialized_item = MenuItemSerializer(item, data=request.data, partial=True)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data)
      elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
  
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def managers(request):
  if request.user.groups.filter(name='Manager').exists():
    if request.method == 'GET':
      managers = User.objects.filter(groups__name='Manager')
      serialized_managers = UserSerializer(managers, many=True)
      return Response(serialized_managers.data)
    elif request.method == 'POST':
      username = request.data.get('username')
      user = get_object_or_404(User, username=username)
      managers = Group.objects.get(name='Manager')
      managers.user_set.add(user)
      return Response(status=status.HTTP_201_CREATED)
  return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_manager(request, pk):
  if request.user.groups.filter(name='Manager').exists():
    if request.method == 'DELETE':
      user = get_object_or_404(User, pk=pk)
      managers = Group.objects.get(name='Manager')
      managers.user_set.remove(user)
      return Response(status=status.HTTP_204_NO_CONTENT)
  return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def delivery_crews(request):
  if request.user.groups.filter(name='Manager').exists():
    if request.method == 'GET':
      delivery_crews = User.objects.filter(groups__name='Delivery crew')
      serialized_delivery_crews = UserSerializer(delivery_crews, many=True)
      return Response(serialized_delivery_crews.data)
    elif request.method == 'POST':
      username = request.data.get('username')
      user = get_object_or_404(User, username=username)
      delivery_crews = Group.objects.get(name='Delivery crew')
      delivery_crews.user_set.add(user)
      return Response(status=status.HTTP_201_CREATED)
  return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_delivery_crew(request, pk):
  if request.user.groups.filter(name='Manager').exists():
    if request.method == 'DELETE':
      user = get_object_or_404(User, pk=pk)
      delivery_crews = Group.objects.get(name='Delivery crew')
      delivery_crews.user_set.remove(user)
      return Response(status=status.HTTP_204_NO_CONTENT)
  return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def cart_menu_items(request):
  if request.method == 'GET':
    cart_menu_items = Cart.objects.filter(user=request.user.id)
    serialized_cart_menu_items = CartSerializer(cart_menu_items, many=True)
    return Response(serialized_cart_menu_items.data)
  elif request.method == 'POST':
    serialized_cart = CartSerializer(data=request.data)
    serialized_cart.is_valid(raise_exception=True)
    serialized_cart.save()
    return Response(serialized_cart.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_cart_menu_item(request, pk):
  if request.method == 'DELETE':
    cart_menu_item = get_object_or_404(Cart, pk=pk)
    cart_menu_item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def orders(request):
  if request.method == 'GET':
    if request.user.groups.filter(name='Manager').exists():
      orders = Order.objects.select_related('user','delivery_crew').all()
      serialized_orders = OrderSerializer(orders, many=True)
      return Response(serialized_orders.data)
    elif request.user.groups.filter(name='Delivery crew').exists():
      orders = Order.objects.select_related('user','delivery_crew').filter(delivery_crew=request.user.id)
      serialized_orders = OrderSerializer(orders, many=True)
      return Response(serialized_orders.data)
    else:
      orders = Order.objects.select_related('user','delivery_crew').filter(user=request.user.id)
      serialized_orders = OrderSerializer(orders, many=True)
      return Response(serialized_orders.data)