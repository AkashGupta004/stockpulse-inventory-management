from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """
    Form for creating and editing Products with Bootstrap styling and custom validation.
    """
    class Meta:
        model = Product
        fields = [
            'name',
            'sku',
            'category',
            'description',
            'purchase_price',
            'selling_price',
            'stock_quantity',
            'supplier_name',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Wireless Ergonomic Mouse',
                'required': True,
                'id': 'product-name-input',
            }),
            'sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. ELEC-MOU-001',
                'required': True,
                'id': 'product-sku-input',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
                'id': 'product-category-input',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Provide specifications, details, or notes about the product...',
                'id': 'product-description-input',
            }),
            'purchase_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
                'required': True,
                'id': 'product-purchase-price-input',
            }),
            'selling_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
                'required': True,
                'id': 'product-selling-price-input',
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0',
                'required': True,
                'id': 'product-stock-input',
            }),
            'supplier_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Logitech Global Supply',
                'required': True,
                'id': 'product-supplier-input',
            }),
        }

    def clean_sku(self):
        sku = self.cleaned_data.get('sku', '').strip()
        if not sku:
            raise ValidationError("SKU / Product ID cannot be empty.")

        # Check for case-insensitive duplicate SKU, excluding current product if updating
        existing = Product.objects.filter(sku__iexact=sku)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise ValidationError(f"A product with SKU '{sku}' already exists. SKU must be unique.")
        return sku

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise ValidationError("Product name must be at least 2 characters long.")
        return name

    def clean(self):
        cleaned_data = super().clean()
        purchase_price = cleaned_data.get('purchase_price')
        selling_price = cleaned_data.get('selling_price')

        if purchase_price is not None and purchase_price < 0:
            self.add_error('purchase_price', "Purchase price cannot be negative.")

        if selling_price is not None and selling_price < 0:
            self.add_error('selling_price', "Selling price cannot be negative.")

        # Non-blocking note or check: selling price less than purchase price
        if purchase_price is not None and selling_price is not None:
            if selling_price < purchase_price:
                # Still allowed (e.g. clearance sale), but we could warn or flag.
                pass

        return cleaned_data


class CategoryForm(forms.ModelForm):
    """
    Form for creating and managing Categories.
    """
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Office Equipment',
                'required': True,
                'id': 'category-name-input',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Category description or group purpose...',
                'id': 'category-description-input',
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError("Category name cannot be empty.")

        existing = Category.objects.filter(name__iexact=name)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise ValidationError(f"Category '{name}' already exists.")
        return name
