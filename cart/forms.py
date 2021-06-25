from django import forms

class CartAddProductForm(forms.Form):
    quantity = forms.CharField(widget=forms.NumberInput(attrs={'size':4, 'class':'input-text qty text', 'title':'Qty', 'value':1, 'min':1, 'max':10, 'step':1}))
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)