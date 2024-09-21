from django.urls import path
from . import views
from . import views
urlpatterns = [
path('update/<int:pk>/', views.update_medicine, name='update_medicine'),
path('delete/<int:pk>/', views.delete_medicine, name='delete_medicine'),
]