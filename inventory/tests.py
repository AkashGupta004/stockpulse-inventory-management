from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Product


class InventoryModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Hardware",
            description="Computer components and parts"
        )
        self.product = Product.objects.create(
            name="Test Solid State Drive 1TB",
            sku="SSD-TEST-001",
            category=self.category,
            description="NVMe PCIe 4.0 SSD",
            purchase_price=Decimal("60.00"),
            selling_price=Decimal("95.00"),
            stock_quantity=15,
            supplier_name="Samsung Memory Corp",
        )

    def test_model_properties_and_calculations(self):
        # Total inventory value: 60 * 15 = 900
        self.assertEqual(self.product.total_inventory_value, Decimal("900.00"))
        # Potential revenue: 95 * 15 = 1425
        self.assertEqual(self.product.potential_revenue, Decimal("1425.00"))
        # Profit per unit: 95 - 60 = 35
        self.assertEqual(self.product.profit_per_unit, Decimal("35.00"))
        # Stock status
        self.assertEqual(self.product.stock_status, "In Stock")
        self.assertFalse(self.product.is_low_stock)
        self.assertFalse(self.product.is_out_of_stock)

    def test_low_stock_and_out_of_stock_thresholds(self):
        # Low stock: stock between 1 and 9
        self.product.stock_quantity = 5
        self.product.save()
        self.assertTrue(self.product.is_low_stock)
        self.assertEqual(self.product.stock_status, "Low Stock")

        # Out of stock: 0
        self.product.stock_quantity = 0
        self.product.save()
        self.assertTrue(self.product.is_out_of_stock)
        self.assertEqual(self.product.stock_status, "Out of Stock")


class InventoryViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Electronics",
            description="Consumer electronics"
        )
        self.prod1 = Product.objects.create(
            name="Wireless Mouse",
            sku="MOU-001",
            category=self.category,
            purchase_price=Decimal("20.00"),
            selling_price=Decimal("35.00"),
            stock_quantity=15,
            supplier_name="Logitech",
        )
        self.prod2 = Product.objects.create(
            name="Mechanical Keyboard",
            sku="KEY-002",
            category=self.category,
            purchase_price=Decimal("50.00"),
            selling_price=Decimal("80.00"),
            stock_quantity=4,  # Low stock
            supplier_name="Keychron",
        )
        self.prod3 = Product.objects.create(
            name="Monitor Arm",
            sku="ARM-003",
            category=self.category,
            purchase_price=Decimal("30.00"),
            selling_price=Decimal("55.00"),
            stock_quantity=0,  # Out of stock
            supplier_name="ErgoTech",
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inventory Dashboard")
        self.assertEqual(response.context['total_products'], 3)
        self.assertEqual(response.context['low_stock_count'], 1)
        self.assertEqual(response.context['out_of_stock_count'], 1)
        # Total value: (20*15) + (50*4) + (30*0) = 300 + 200 + 0 = 500
        self.assertEqual(response.context['total_inventory_value'], Decimal("500.00"))

    def test_product_list_view_and_filtering(self):
        # All products
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 3)

        # Search by SKU
        response = self.client.get(reverse('product_list'), {'q': 'MOU-001'})
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0].name, "Wireless Mouse")

        # Search by Name
        response = self.client.get(reverse('product_list'), {'q': 'Keyboard'})
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0].sku, "KEY-002")

        # Filter low stock
        response = self.client.get(reverse('product_list'), {'status': 'low_stock'})
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0].sku, "KEY-002")

        # Filter out of stock
        response = self.client.get(reverse('product_list'), {'status': 'out_of_stock'})
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0].sku, "ARM-003")

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.prod1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wireless Mouse")
        self.assertContains(response, "MOU-001")

        # Non-existent ID returns 404
        response404 = self.client.get(reverse('product_detail', args=[99999]))
        self.assertEqual(response404.status_code, 404)

    def test_product_create_and_validation(self):
        # GET create page
        response = self.client.get(reverse('product_create'))
        self.assertEqual(response.status_code, 200)

        # POST valid product
        post_data = {
            'name': 'USB-C Hub Multiport',
            'sku': 'HUB-004',
            'category': self.category.pk,
            'description': '7-in-1 USB C Hub with HDMI 4K',
            'purchase_price': '25.00',
            'selling_price': '45.00',
            'stock_quantity': '30',
            'supplier_name': 'Anker',
        }
        response = self.client.post(reverse('product_create'), post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Product.objects.filter(sku='HUB-004').exists())

        # POST duplicate SKU should fail
        response_dup = self.client.post(reverse('product_create'), post_data)
        self.assertEqual(response_dup.status_code, 200)
        self.assertFormError(response_dup.context['form'], 'sku', "A product with SKU 'HUB-004' already exists. SKU must be unique.")

        # POST negative price should fail
        bad_data = post_data.copy()
        bad_data['sku'] = 'HUB-005'
        bad_data['purchase_price'] = '-10.00'
        response_neg = self.client.post(reverse('product_create'), bad_data)
        self.assertEqual(response_neg.status_code, 200)
        self.assertFormError(response_neg.context['form'], 'purchase_price', "Purchase price cannot be negative.")

    def test_product_edit(self):
        edit_url = reverse('product_edit', args=[self.prod1.pk])
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)

        update_data = {
            'name': 'Wireless Ergonomic Mouse V2',
            'sku': 'MOU-001',
            'category': self.category.pk,
            'description': 'Updated model',
            'purchase_price': '22.00',
            'selling_price': '39.99',
            'stock_quantity': '18',
            'supplier_name': 'Logitech',
        }
        response = self.client.post(edit_url, update_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.prod1.refresh_from_db()
        self.assertEqual(self.prod1.name, 'Wireless Ergonomic Mouse V2')
        self.assertEqual(self.prod1.stock_quantity, 18)

    def test_product_delete(self):
        delete_url = reverse('product_delete', args=[self.prod1.pk])
        # GET confirmation page
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Confirm Product Deletion")

        # POST delete
        response = self.client.post(delete_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Product.objects.filter(pk=self.prod1.pk).exists())

    def test_category_management(self):
        # Category list view
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)

        # Create category
        response = self.client.post(reverse('category_list'), {
            'name': 'Pantry Supplies',
            'description': 'Snacks and drinks'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Category.objects.filter(name='Pantry Supplies').exists())

        # Duplicate category name fails
        response_dup = self.client.post(reverse('category_list'), {
            'name': 'Pantry Supplies',
            'description': 'Duplicate'
        })
        self.assertFormError(response_dup.context['form'], 'name', "Category 'Pantry Supplies' already exists.")
