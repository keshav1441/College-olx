from django.shortcuts import get_object_or_404,render, redirect
from django.http import HttpResponse
from .models import Product, Category, ProductImage
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/product.html',{
        'products' : products,
        'categories' : categories
    })


def sell(request):
    categories = Category.objects.all()
    return render(request, 'products/sell.html', {'categories': categories})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_details.html', {'product': product})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products_in_category = Product.objects.filter(category=category)
    return render(request, 'products/category_detail.html', {
        'category': category,
        'products': products_in_category
    })

def about(request):
    return render(request, 'products/about.html')


def sell_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        product_description = request.POST.get('product_description')
        images = request.FILES.getlist('product_images')  # Get the list of files

        if not product_name or not category_id or not price or not product_description:
            # Assuming you have a way to display error messages on your template
            return render(request, 'your_template_name.html', {
                'error_message': "All fields are required.",
                'categories': Category.objects.all(),
            })

        if len(images) > 10:
            return HttpResponse("You can't upload more than 10 images.", status=400)

        try:
            category = Category.objects.get(uid=category_id)
        except Category.DoesNotExist:
            return HttpResponse("Category does not exist.", status=400)

        try:
            price = int(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            return HttpResponse("Invalid price.", status=400)

        # Create and save the product instance
        product = Product(
            seller=request.user,
            product_name=product_name,
            category=category,
            price=price,
            product_description=product_description
        )
        product.save()  # Save the product before adding images

        # Save each image
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        # Redirect to the products listing page, assuming the name of the url is 'products:index'
        return redirect('products:index')
    else:
        categories = Category.objects.all()
        # Update 'your_template_name.html' to your actual template name for the sell product page
        return render(request, 'your_template_name.html', {'categories': categories})