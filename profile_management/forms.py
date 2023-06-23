from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """A form for user information"""
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """ Add placeholders and  set autofoucs to first field"""
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_address1': 'Address Line 1',
            'default_address2': 'Address Line 2',
            'default_city': 'City',
            'default_county': 'County',
            'default_postal_code': 'Postal Code',
        }
        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
