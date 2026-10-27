# 📦 Inventory Management System (StockPulse)

A complete, production-ready **Inventory Management System** built with **Python Django**, **SQLite**, **HTML5**, **CSS3**, and **Bootstrap 5**. Designed with a modern dashboard, responsive sidebar, real-time KPI metrics, stock alerts, multi-criteria filtering, and full CRUD operations.

---

## 🚀 Key Features

### 1. Core CRUD Operations
- **Add Products**: Add new inventory items with custom validation, pricing, categories, and suppliers.
- **View All Products**: High-density, responsive data table with status badges and stock indicators.
- **Product Details**: Dedicated page with unit economics, profit margins, stock health gauge, and audit timestamps.
- **Edit Products**: Update product pricing, suppliers, stock counts, and descriptions.
- **Delete Products**: Secure deletion with interactive Bootstrap modal and standalone confirmation page.

### 2. Product Fields
| Field | Type | Description |
|---|---|---|
| **Product Name** | `CharField` | Clear name of the product |
| **SKU / Product ID** | `CharField (Unique)` | Unique stock identifier (e.g. `ELEC-MON-4K01`) |
| **Category** | `ForeignKey` | Relation to Category model |
| **Description** | `TextField` | Detailed specs, color, or notes |
| **Purchase Price** | `DecimalField` | Cost price paid to vendor (non-negative) |
| **Selling Price** | `DecimalField` | Retail price charged to customers (non-negative) |
| **Stock Quantity** | `IntegerField` | Units on hand (non-negative) |
| **Supplier Name** | `CharField` | Name of distributor or manufacturer |
| **Date Added** | `DateTimeField` | Automatically recorded creation timestamp |

### 3. Real-Time Dashboard
- **Total Products**: Live count of all active catalog items.
- **Total Inventory Value**: Aggregated purchase valuation (`Purchase Price × Stock Quantity`).
- **Potential Sales Revenue**: Forecasted revenue (`Selling Price × Stock Quantity`).
- **Low Stock Alerts**: Real-time counter and table of items below 10 units threshold.
- **Out of Stock Alerts**: Real-time counter and table of items with 0 stock.
- **Recently Added Products Table**: Quick access to newly created stock items with action buttons.
- **Category Breakdown**: Progress bars and product counts per category.

### 4. Advanced Search & Filtering
- **Search**: Case-insensitive search by product name, SKU, or supplier name.
- **Filter by Category**: Dynamic dropdown populated from database categories.
- **Filter by Stock Status**: Quick toggle between All, In Stock, Low Stock (<10), and Out of Stock (0).
- **Multi-Sort**: Sort by Date Added (Newest/Oldest), Name (A-Z/Z-A), Price, or Stock level.
- **Pagination**: 10 items per page with query string preservation across page links.

### 5. Categories Management
- Dedicated Category CRUD: Create, View, Edit, and Delete categories.
- Tracks live product counts per category with cascade deletion warnings.

### 6. Django Admin Integration
- Built-in Django Admin registered with filters, search fields, date hierarchy, and calculated metrics.

---

## 🛠️ Tech Stack & Architecture

- **Backend**: Python 3.10+ / Django 5+ / Django 6+
- **Database**: SQLite3 (`db.sqlite3`)
- **Frontend**: HTML5, Vanilla CSS3, Bootstrap 5.3.3, Bootstrap Icons 1.11.3
- **Architecture**: Model-View-Template (MVT) with Django ORM and Django Forms

---

## 💻 Quick Setup & Execution Guide (Windows / macOS / Linux)

### 1. Clone the Repository
```bash
git clone https://github.com/AkashGupta004/stockpulse-inventory-management.git
cd stockpulse-inventory-management
```

### 2. Create and Activate a Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
  *(If PowerShell displays a script execution policy notice, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*
- **Windows (Command Prompt / CMD)**:
  ```cmd
  python -m venv venv
  venv\Scripts\activate.bat
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Seed Realistic Sample Data & Default Admin Superuser
Populates 15 realistic products across 5 categories and creates the default admin superuser:
```bash
python manage.py seed_inventory
```

### 6. Start the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
- **Application Dashboard**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **All Products**: [http://127.0.0.1:8000/products/](http://127.0.0.1:8000/products/)
- **Add Product**: [http://127.0.0.1:8000/products/add/](http://127.0.0.1:8000/products/add/)
- **Categories**: [http://127.0.0.1:8000/categories/](http://127.0.0.1:8000/categories/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🔑 Default Administrator Login (Django Admin)

A default superuser is pre-configured for instant testing:
- **Username**: `admin`
- **Password**: `admin123`
- **Admin Portal**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🧪 Running Unit Tests

Run the built-in test suite covering models, CRUD operations, filters, pagination, and calculations:
```powershell
python manage.py test
```

Expected result:
```text
Ran 9 tests in 0.126s
OK
```

---

## 📂 Project Structure

```text
CRUD application/
│
├── inventory_management/         # Django Project Root
│   ├── __init__.py
│   ├── settings.py              # App config, database, static files, message tags
│   ├── urls.py                  # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── inventory/                   # Inventory Core App
│   ├── management/
│   │   └── commands/
│   │       └── seed_inventory.py# Custom data seeder (15 products, 5 categories)
│   ├── migrations/              # Database schema migrations
│   │   └── 0001_initial.py
│   ├── templates/inventory/     # Clean Bootstrap 5 templates
│   │   ├── base.html            # Main layout with responsive sidebar and navbar
│   │   ├── dashboard.html       # Metric cards, recent products, stock alerts
│   │   ├── product_list.html    # Table, search, filter pills, delete modal, pagination
│   │   ├── product_detail.html  # Full product specs, profit margins, stock status
│   │   ├── product_form.html    # Reusable Add & Edit product form
│   │   ├── product_confirm_delete.html # Standalone delete confirmation
│   │   ├── category_list.html   # Categories table & create form
│   │   ├── category_edit.html   # Edit category
│   │   └── category_confirm_delete.html # Delete category with cascade warnings
│   ├── admin.py                 # Django admin registration
│   ├── apps.py                  # App configuration
│   ├── forms.py                 # ProductForm & CategoryForm with validation
│   ├── models.py                # Category & Product models
│   ├── tests.py                 # Unit test suite
│   ├── urls.py                  # App URL endpoints
│   └── views.py                 # Dashboard, CRUD views, and aggregations
│
├── static/
│   └── css/
│       └── style.css            # Custom styling, shadows, badge pills, animations
│
├── db.sqlite3                   # SQLite database
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
└── README.md                    # Setup and documentation guide
```
