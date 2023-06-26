from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .forms import ProductForm, CommentForm, ApproveCommentForm, ContactForm, NewsletterForm
from .models import Comment, Contact, Newsletter


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
    product = get_object_or_404(Product, pk=product_id)
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


@login_required
def view_comments(request):
    """ A view that renders users comments"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners\
             are allowed on this page!')
        return redirect(reverse('home'))
    comments = Comment.objects.all()
    context = {
        'comments': comments,
    }
    return render(request, 'store_management/view_comments.html', context)


@login_required
def approve_comment(request, comment_id):
    """ A view to approve comments on store products """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners\
             are allowed on this page!')
        return redirect(reverse('home'))
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = ApproveCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.info(request, 'Comment has been approved.')
            return redirect(reverse('view_comments'))
        else:
            messages.error(request, 'Unable to approve comment.\
                            Please check form is valid.')
    else:
        form = ApproveCommentForm(instance=comment)
    context = {
        'form': form,
        'comment': comment,
    }
    return render(request, 'store_management/approve_comment.html', context)


@login_required
def delete_comment(request, comment_id):
    """ Delete Unapproved comments from the website """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners are allowed on\
             this page!')
        return redirect(reverse('home'))
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    messages.info(request, 'Comment deleted successfully.')
    return redirect(reverse('view_comments'))


@login_required
def contact_form(request):
    """ Contact form view """
    contact_form = ContactForm()
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            customer = contact_form.save(commit=False)
            customer.user = request.user
            contact_form.save()
            messages.info(request, 'Message sent successfully, a member of\
                staff will get back to you shortly.')
            return redirect(reverse('home',))

        else:
            messages.error(request, 'Unable to send message.\
                            Please check form is valid.')
    else:
        contact_form = ContactForm()
    context = {
        'contact_form': contact_form,
    }
    return render(request, 'store_management/contact_form.html', context)


@login_required
def store_inbox(request):
    """ A view that renders all the store's messages """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners\
             are allowed on this page!')
        return redirect(reverse('home'))
    mails = Contact.objects.all()
    context = {
        'mails': mails,
    }
    return render(request, 'store_management/store_inbox.html', context)


@login_required
def delete_message(request, message_id):
    """ Delete messages from the store's inbox"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners are allowed\
             on this page!')
        return redirect(reverse('home'))
    mail = get_object_or_404(Contact, pk=message_id)
    mail.delete()
    messages.info(request, 'Message deleted successfully.')
    return redirect(reverse('store_inbox'))


def newsletter(request):
    """ A view that renders a newsletter form """
    form = NewsletterForm()
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Subscribed successfully')
            return redirect(reverse('home'))
        else:
            messages.error(request, 'Unable to send message.\
                            Please check form is valid.')
    else:
        form = NewsletterForm()
    context = {
        'form': form,
    }
    return context
