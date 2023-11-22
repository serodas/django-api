from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer

class CategoriesView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@api_view(['GET', 'POST'])
def menu_items(request):   
  if request.method == 'GET':
    items = MenuItem.objects.select_related('category').all()
    serialized_items = MenuItemSerializer(items, many=True)
    return Response(serialized_items.data)
  if request.method == 'POST':
    if request.user.groups.filter(name='Manager').exists():
      serialized_item = MenuItemSerializer(data=request.data)
      serialized_item.is_valid(raise_exception=True)
      serialized_item.save()
      return Response(serialized_item.data, status=status.HTTP_201_CREATED)
    return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
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