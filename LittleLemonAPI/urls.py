from django.urls import path
from . import views

urlpatterns = [
  path('categories', views.CategoriesView.as_view()),
  path('menu-items', views.menu_items),
  path('menu-items/<int:pk>', views.menu_item),
]