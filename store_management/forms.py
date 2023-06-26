from django import forms
from products.models import Product
from .widgets import CustomClearableFileInput
from .models import Comment


class ProductForm(forms.ModelForm):
    """ A form to add a new products """
    class Meta:
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
