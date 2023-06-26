from django.shortcuts import render, reverse, redirect, get_object_or_404
from .forms import ProductForm, CommentForm
from products.models import Product, Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def add_product(request):
    """ Add's products to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners are\
             allowed on this page!')
        return redirect(reverse('home'))
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


@login_required
def edit_product(request, product_id):
    """ Edit product's in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners are\
             allowed on this page!')
        return redirect(reverse('home'))
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.info(request, 'Product updated successfully.')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Unable to update product.\
                            Please check form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing this product\
             ({ product.name }). All products added to the store\
                 must have an image.')
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'store_management/edit_product.html', context)


@login_required
def delete_product(request, product_id):
    """ Delete product's from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners are\
             allowed on this page!')
        return redirect(reverse('home'))
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.info(request, 'Product deleted successfully.')
    return redirect(reverse('products'))


@login_required
def add_comment(request, product_id):
    """ A view to comment on store products """
    product = get_object_or_404(Product, id=product_id)
    user_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.product = product
            user_comment.user = request.user
            user_comment.save()
            messages.info(request, 'Your comment will be posted here shortly,\
                once it has been approved.')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Unable to post comment.\
                            Please check form is valid.')
    else:
        comment_form = CommentForm()
        messages.info(request, f'You are adding a comment to this product\
             ({ product.name })')
    context = {
        'comment_form': comment_form,
        'user_comment': user_comment,
    }
    return render(request, 'store_management/add_comment.html', context)
