from django import forms
from home.models import ( Category, Product)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def clean_title(self):
        title= self.cleaned_data.get('title')
        if Category.objects.filter(title__iexact=title).exists():
            raise forms.ValidationError('Category already exists')
        return title
    
class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['image','title', 'category', 'quantity', 'price', 'description']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
    def clean_quantity(self):
        quantity= self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 1:
            raise forms.ValidationError('Quantity must be greater than 1')
        return quantity
    
    def clean_price(self):
        price= self.cleaned_data.get('price')
        if price is not None and price < 1:
            raise forms.ValidationError('Price must be greater than 1')
        return price
