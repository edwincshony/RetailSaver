from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'weight_unit', 'amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Red Apple'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 5'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Save Product', css_class='btn btn-primary w-100'))
        self.fields['weight_unit'].widget.attrs['class'] = 'form-select'
