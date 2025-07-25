from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('product/<int:id>/', views.product_detail, name='product_detail'),  # Product detail
]
