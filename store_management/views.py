from django.shortcuts import render, reverse, redirect, get_object_or_404
from .forms import ProductForm
from django.contrib import messages


def add_product(request):
    """ Add's products to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.info(request, 'Product added successfully!')
            return redirect(reverse('products'))
        else:
            messages.error(request, 'Unable to add product.\
                            Please check form is valid.')
    else:
        form = ProductForm()
    context = {
        'form': form,
    }
    return render(request, 'store_management/add_product.html', context)
