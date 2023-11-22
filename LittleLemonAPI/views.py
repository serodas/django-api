from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer

class CategoriesView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
      permission_classes = []
      if self.request.method != 'GET':
        permission_classes = [IsAdminUser]
      return [permission() for permission in permission_classes]
    
class MenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
      permission_classes = []
      if self.request.method != 'GET':
        permission_classes = [IsAdminUser]
      return [permission() for permission in permission_classes]