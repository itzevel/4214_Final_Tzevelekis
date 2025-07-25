from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# Home page: Show all products
def home(request):
    products = Product.objects.all()  # Fetch all products
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'shop/home.html', {'products': products, 'categories': categories})

# Product detail page: Show single product
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product': product})
