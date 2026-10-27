from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """
    Category model for classifying inventory items.
    """
    name = models.CharField(max_length=100, unique=True, help_text="Category name (e.g. Electronics, Furniture)")
    description = models.TextField(blank=True, help_text="Brief description of the category")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def product_count(self):
        return self.products.count()


class Product(models.Model):
    """
    Product model storing complete item and inventory tracking details.
    """
    name = models.CharField(max_length=200, help_text="Name of the product")
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU / Product ID", help_text="Unique Stock Keeping Unit")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True, help_text="Detailed description of the product")
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Cost price paid to supplier (USD)"
    )
    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Retail selling price for customers (USD)"
    )
    stock_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Current number of units in stock"
    )
    supplier_name = models.CharField(max_length=150, help_text="Name of the vendor or supplier")
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def total_inventory_value(self):
        """Total cost value of this item in current stock."""
        return self.purchase_price * self.stock_quantity

    @property
    def potential_revenue(self):
        """Total potential sales value of current stock."""
        return self.selling_price * self.stock_quantity

    @property
    def profit_per_unit(self):
        """Profit made per unit sold."""
        return self.selling_price - self.purchase_price

    @property
    def profit_margin_percent(self):
        """Profit margin percentage based on purchase price."""
        if self.purchase_price > Decimal('0.00'):
            margin = ((self.selling_price - self.purchase_price) / self.purchase_price) * 100
            return round(margin, 1)
        return 0.0

    @property
    def is_out_of_stock(self):
        return self.stock_quantity == 0

    @property
    def is_low_stock(self):
        return 0 < self.stock_quantity < 10

    @property
    def stock_status(self):
        if self.stock_quantity == 0:
            return "Out of Stock"
        elif self.stock_quantity < 10:
            return "Low Stock"
        return "In Stock"

    @property
    def stock_badge_class(self):
        if self.stock_quantity == 0:
            return "badge-out-of-stock"
        elif self.stock_quantity < 10:
            return "badge-low-stock"
        return "badge-in-stock"
