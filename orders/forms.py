from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields =  ['first_name', 'last_name', 'address', 'city', 'county', 'postal_code', 'email', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input-text'

        self.fields['city'].widget.attrs['placeholder'] = 'Town / City'
        self.fields['county'].widget.attrs['placeholder'] = 'State / County'
        self.fields['postal_code'].widget.attrs['placeholder'] = 'Postcode / Zip'