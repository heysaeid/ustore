from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'input-text'}))

    class Meta:
        model = Order
        fields =  ['first_name', 'last_name', 'address', 'city', 'county', 'postal_code', 'phone', 'email', 'password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input-text'

        if self.request.user.is_authenticated:
            self.fields['password'].required = False

        self.fields['city'].widget.attrs['placeholder'] = 'Town / City'
        self.fields['county'].widget.attrs['placeholder'] = 'State / County'
        self.fields['postal_code'].widget.attrs['placeholder'] = 'Postcode / Zip'