from django.urls import path
from . import views

urlpatterns = [
  path('categories', views.CategoriesView.as_view()),
  path('menu-items', views.menu_items),
  path('menu-items/<int:pk>', views.menu_item),
  path('groups/manager/users', views.managers),
  path('groups/manager/users/<int:pk>', views.remove_manager),
  path('groups/delivery-crew/users', views.delivery_crews),
  path('groups/delivery-crew/users/<int:pk>', views.remove_delivery_crew),
  path('cart/menu-items', views.cart_menu_items),
]