from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Avg
from .models import Product, Category, CartItem, Review
from .forms import RegisterForm

# Home page: Show all products
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Get filter values
    query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    brand_filter = request.GET.get('brand', '').strip()

    # Apply search filter
    if query:
        products = products.filter(name__icontains=query)

    # Apply category filter (only if it's not empty or "All")
    if category_filter and category_filter.lower() != 'all':
        products = products.filter(category__name__iexact=category_filter)

    # Apply brand filter
    if brand_filter:
        products = products.filter(brand__icontains=brand_filter)

    # Apply price filters
    if min_price.isdigit():
        products = products.filter(price__gte=float(min_price))
    if max_price.isdigit():
        products = products.filter(price__lte=float(max_price))

    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'category_filter': category_filter,
        'min_price': min_price,
        'max_price': max_price,
        'brand_filter': brand_filter,
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    
    # Calculate average rating
    avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    # Related products (same category, excluding current product)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'avg_rating': round(avg_rating, 1),
        'related_products': related_products
    })


# Register new user
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'shop/register.html', {'form': form})

# Dashboard for logged-in users
@login_required
def dashboard(request):
    return render(request, 'shop/dashboard.html')

# Add to Cart
@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

# View Cart
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})

# Remove item from cart
@login_required
def remove_from_cart(request, id):
    cart_item = get_object_or_404(CartItem, id=id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')

# Add review via AJAX
@login_required
def add_review(request, id):
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '')

        product = get_object_or_404(Product, id=id)

        
        review, created = Review.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={'rating': rating, 'comment': comment}
        )

    
        avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']

        return JsonResponse({'success': True, 'avg_rating': round(avg_rating, 1)})
    return JsonResponse({'success': False}, status=400)
