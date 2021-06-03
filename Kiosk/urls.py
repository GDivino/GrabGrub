from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.log_in, name='log_in'),
    path('signup', views.signup, name='signup'),
    path('view_order', views.view_order, name='view_order'),
    path('view_order_detail/<int:pk>/', views.view_order_detail, name='view_order_detail'),
    path('add_order', views.add_order, name='add_order'),
    path('update_order/<int:pk>/', views.update_order, name='update_order'),
    path('delete_order/<int:pk>/', views.delete_order, name='delete_order'),
    path('view_food', views.view_food, name='view_food'),
    path('add_food', views.add_food, name='add_food'),
    path('view_food_details/<int:pk>/', views.view_food_details, name='view_food_details'),
    path('update_food_details/<int:pk>/', views.update_food_details, name='update_food_details'),
    path('delete_food/<int:pk>/', views.delete_food, name='delete_food'),
    path('view_customer', views.view_customer, name='view_customer'),
    path('add_customer', views.add_customer, name='add_customer'),
    path('view_customer_details/<int:pk>/', views.view_customer_details, name='view_customer_details'),
    path('update_customer_details/<int:pk>/', views.update_customer_details, name='update_customer_details'),
    path('delete_customer/<int:pk>/', views.delete_customer, name='delete_customer'),
]