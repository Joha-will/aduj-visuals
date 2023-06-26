from django import forms
from products.models import Product
from .widgets import CustomClearableFileInput
from .models import Comment, Contact


class ProductForm(forms.ModelForm):
    """ A form to add a new products """
    class Meta:
        """ Assign model and fields"""
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Name',
            'model_name': 'Model Name',
            'category': 'Category',
            'description': 'Description',
            'size': 'Size',
            'image': 'Image',
            'price': 'Price',
        }
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False


class CommentForm(forms.ModelForm):
    """ A form for users to make commments """

    class Meta:
        """ Assign model and fields"""
        model = Comment
        fields = ('title', 'user_name', 'content', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'title': 'Title',
            'user_name': 'Username',
            'content': 'Comment',
        }
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False


class ApproveCommentForm(forms.ModelForm):
    """ A form for admins to approve comments"""
    class Meta:
        """ Assign model and fields"""
        model = Comment
        fields = ('title', 'user_name', 'content', 'approved',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'title': 'title',
            'user_name': 'Username',
            'content': 'Comment',
            'approved': 'Approved'
        }
        for field in self.fields:
            self.fields[field].widget.attrs = {'readonly': 'readonly'}
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
            self.fields['approved'].label = 'Approve comment'


class ContactForm(forms.ModelForm):
    """ A form for users contact information """
    class Meta:
        """ Assign model and fields"""
        model = Contact
        fields = '__all__'
        exclude = ('sent_on', 'user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Name',
            'email_address': 'Email',
            'tel_number': 'Tel No.',
            'message': 'Message',
        }
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
