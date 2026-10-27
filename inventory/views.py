from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum, F, Q, Count, DecimalField
from django.db.models.functions import Coalesce

from .models import Product, Category
from .forms import ProductForm, CategoryForm


def dashboard(request):
    """
    Main dashboard displaying real-time metrics, KPI cards, low stock alerts,
    and recently added products.
    """
    total_products = Product.objects.count()
    total_categories = Category.objects.count()

    # Calculate total inventory value: purchase_price * stock_quantity
    inventory_val_agg = Product.objects.aggregate(
        total_value=Coalesce(
            Sum(F('purchase_price') * F('stock_quantity'), output_field=DecimalField(max_digits=12, decimal_places=2)),
            Decimal('0.00')
        ),
        potential_revenue=Coalesce(
            Sum(F('selling_price') * F('stock_quantity'), output_field=DecimalField(max_digits=12, decimal_places=2)),
            Decimal('0.00')
        ),
        total_items_in_stock=Coalesce(Sum('stock_quantity'), 0)
    )

    total_inventory_value = inventory_val_agg['total_value']
    total_potential_revenue = inventory_val_agg['potential_revenue']
    total_items_in_stock = inventory_val_agg['total_items_in_stock']

    # Low-stock (quantity > 0 and < 10) and out-of-stock (quantity == 0)
    low_stock_count = Product.objects.filter(stock_quantity__gt=0, stock_quantity__lt=10).count()
    out_of_stock_count = Product.objects.filter(stock_quantity=0).count()
    in_stock_count = Product.objects.filter(stock_quantity__gte=10).count()

    # Recently added products (latest 6)
    recent_products = Product.objects.select_related('category').order_by('-date_added')[:6]

    # Critical low stock items needing immediate reorder (low stock or out of stock, top 5)
    urgent_reorders = Product.objects.select_related('category').filter(stock_quantity__lt=10).order_by('stock_quantity')[:5]

    # Category breakdown for insights
    categories_summary = Category.objects.annotate(
        num_products=Count('products')
    ).order_by('-num_products')[:5]

    context = {
        'total_products': total_products,
        'total_inventory_value': total_inventory_value,
        'total_potential_revenue': total_potential_revenue,
        'total_items_in_stock': total_items_in_stock,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'in_stock_count': in_stock_count,
        'total_categories': total_categories,
        'recent_products': recent_products,
        'urgent_reorders': urgent_reorders,
        'categories_summary': categories_summary,
        'page_title': 'Inventory Dashboard',
        'active_menu': 'dashboard',
    }
    return render(request, 'inventory/dashboard.html', context)


def product_list(request):
    """
    List all products with comprehensive search, category/stock filtering,
    sorting, and pagination.
    """
    queryset = Product.objects.select_related('category').all()

    # Search by name or SKU
    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) | Q(sku__icontains=query) | Q(supplier_name__icontains=query)
        )

    # Filter by category
    category_id = request.GET.get('category', '').strip()
    selected_category = None
    if category_id:
        queryset = queryset.filter(category_id=category_id)
        selected_category = Category.objects.filter(pk=category_id).first()

    # Filter by stock status
    stock_status = request.GET.get('status', 'all').strip()
    if stock_status == 'low_stock':
        queryset = queryset.filter(stock_quantity__gt=0, stock_quantity__lt=10)
    elif stock_status == 'out_of_stock':
        queryset = queryset.filter(stock_quantity=0)
    elif stock_status == 'in_stock':
        queryset = queryset.filter(stock_quantity__gte=10)

    # Sorting
    sort_by = request.GET.get('sort', 'date_desc')
    sort_mapping = {
        'date_desc': '-date_added',
        'date_asc': 'date_added',
        'name_asc': 'name',
        'name_desc': '-name',
        'price_desc': '-selling_price',
        'price_asc': 'selling_price',
        'stock_asc': 'stock_quantity',
        'stock_desc': '-stock_quantity',
    }
    order_field = sort_mapping.get(sort_by, '-date_added')
    queryset = queryset.order_by(order_field)

    # Total matching count before pagination
    total_count = queryset.count()

    # Pagination: 10 items per page
    paginator = Paginator(queryset, 10)
    page = request.GET.get('page', 1)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # Get all categories for filter dropdown
    categories = Category.objects.all().order_by('name')

    # Count quick stats for tabs/badges
    all_count = Product.objects.count()
    low_stock_count = Product.objects.filter(stock_quantity__gt=0, stock_quantity__lt=10).count()
    out_of_stock_count = Product.objects.filter(stock_quantity=0).count()

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': selected_category,
        'selected_category_id': category_id,
        'stock_status': stock_status,
        'sort_by': sort_by,
        'total_count': total_count,
        'all_count': all_count,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'page_title': 'Products Inventory',
        'active_menu': 'products',
    }
    return render(request, 'inventory/product_list.html', context)


def product_detail(request, pk):
    """
    Detailed view for a single product showing all metadata and calculations.
    """
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    context = {
        'product': product,
        'page_title': f"Product: {product.name}",
        'active_menu': 'products',
    }
    return render(request, 'inventory/product_detail.html', context)


def product_create(request):
    """
    Create a new product. If no categories exist, provides guidance.
    """
    categories_exist = Category.objects.exists()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' (SKU: {product.sku}) was successfully added!")
            return redirect('product_detail', pk=product.pk)
        else:
            messages.error(request, "Please check the form for errors and try again.")
    else:
        # Prepopulate category if passed via query param
        initial_data = {}
        category_id = request.GET.get('category')
        if category_id:
            initial_data['category'] = category_id
        form = ProductForm(initial=initial_data)

    context = {
        'form': form,
        'categories_exist': categories_exist,
        'page_title': 'Add New Product',
        'active_menu': 'add_product',
    }
    return render(request, 'inventory/product_form.html', context)


def product_edit(request, pk):
    """
    Edit an existing product's information.
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' was successfully updated!")
            return redirect('product_detail', pk=product.pk)
        else:
            messages.error(request, "Failed to update product. Please correct the highlighted errors.")
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'is_edit': True,
        'categories_exist': True,
        'page_title': f"Edit Product: {product.name}",
        'active_menu': 'products',
    }
    return render(request, 'inventory/product_form.html', context)


def product_delete(request, pk):
    """
    Delete a product with confirmation message.
    Supports both POST requests and GET confirmation page.
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_name = product.name
        sku = product.sku
        product.delete()
        messages.success(request, f"Product '{product_name}' (SKU: {sku}) has been permanently deleted.")
        return redirect('product_list')

    context = {
        'product': product,
        'page_title': f"Confirm Deletion: {product.name}",
        'active_menu': 'products',
    }
    return render(request, 'inventory/product_confirm_delete.html', context)


def category_list(request):
    """
    Manage categories: view all categories with item counts and add new ones.
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category '{category.name}' created successfully!")
            return redirect('category_list')
        else:
            messages.error(request, "Could not create category. Please fix the error below.")
    else:
        form = CategoryForm()

    categories = Category.objects.annotate(
        product_count_annotated=Count('products')
    ).order_by('name')

    context = {
        'categories': categories,
        'form': form,
        'page_title': 'Categories Management',
        'active_menu': 'categories',
    }
    return render(request, 'inventory/category_list.html', context)


def category_edit(request, pk):
    """
    Edit category name and description.
    """
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category '{category.name}' updated successfully.")
            return redirect('category_list')
        else:
            messages.error(request, "Failed to update category. Please review the errors.")
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
        'page_title': f"Edit Category: {category.name}",
        'active_menu': 'categories',
    }
    return render(request, 'inventory/category_edit.html', context)


def category_delete(request, pk):
    """
    Delete category with safety check on associated products.
    """
    category = get_object_or_404(Category, pk=pk)
    product_count = category.products.count()

    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f"Category '{category_name}' and all its associated products were removed.")
        return redirect('category_list')

    context = {
        'category': category,
        'product_count': product_count,
        'page_title': f"Delete Category: {category.name}",
        'active_menu': 'categories',
    }
    return render(request, 'inventory/category_confirm_delete.html', context)
