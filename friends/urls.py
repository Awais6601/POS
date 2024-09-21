"""
URL configuration for friends project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# project/urls.py
from django.contrib import admin
from django.urls import path,include
from inventory import views  # Import views from the inventory app
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Set the root URL to the home view
    path('add/', views.add_medicine, name='add_medicine'),
    path('inventory/', views.inventory, name='inventory'),
    path('login/', views.login_view, name='login'),  # Map to the login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('inventory/', include('inventory.urls')),  # Ensure this line includes the app's URL configuration
    path('create_order/', views.create_order, name='create_order'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/create/', views.create_transaction, name='create_transaction'),
    path('transactions/<int:pk>/edit/', views.update_transaction, name='update_transaction'),
    path('transactions/<int:pk>/delete/', views.delete_transaction, name='delete_transaction'),
    path('recent/', views.recent_orders, name='recent_orders'),
    path('view_transactions/', views.view_transactions, name='view_transactions'),
    path('search/', views.search_orders, name='search_orders'),  # For search results
    path('export/', views.export_orders_csv, name='export_orders_csv'),
    path('edit/<int:order_id>/', views.edit_order, name='edit_order'),  # Edit order
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),  # Delete order

]
