from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('order/', views.order_online, name='order'),
    path('order/create/', views.create_order, name='create_order'),
    path('booking/', views.table_booking, name='table_booking'),
    path('reviews/', views.reviews, name='reviews'),
    path('contact/', views.contact, name='contact'),
    path('api/menu-item/<int:item_id>/', views.get_menu_item, name='get_menu_item'),
]
