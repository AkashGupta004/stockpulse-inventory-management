from decimal import Decimal
from django.core.management.base import BaseCommand
from inventory.models import Category, Product


class Command(BaseCommand):
    help = "Seeds initial sample categories and products for testing and demonstration"

    def handle(self, *args, **options):
        self.stdout.write("Seeding sample inventory data...")

        # Create Categories
        categories_data = [
            ("Electronics", "Computers, audio, accessories, and mobile hardware"),
            ("Office Supplies", "Stationery, desk equipment, pens, and paper supplies"),
            ("Furniture", "Ergonomic chairs, desks, shelving, and work accessories"),
            ("Networking & IT", "Routers, cables, switches, and server hardware"),
            ("Breakroom & Pantry", "Coffee makers, snacks, cups, and breakroom essentials"),
        ]

        categories_map = {}
        for name, desc in categories_data:
            cat, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
            categories_map[name] = cat
            if created:
                self.stdout.write(f"  + Created Category: {name}")

        # Create Products
        products_data = [
            {
                "name": "Dell UltraSharp 27\" 4K Monitor",
                "sku": "ELEC-MON-4K01",
                "category": "Electronics",
                "description": "High resolution IPS display with USB-C 90W power delivery and color calibration.",
                "purchase_price": Decimal("340.00"),
                "selling_price": Decimal("499.99"),
                "stock_quantity": 24,
                "supplier_name": "Dell Direct Distribution",
            },
            {
                "name": "Logitech MX Master 3S Wireless Mouse",
                "sku": "ELEC-MOU-003",
                "category": "Electronics",
                "description": "Quiet click ergonomic Bluetooth mouse with 8K DPI sensor.",
                "purchase_price": Decimal("62.50"),
                "selling_price": Decimal("99.99"),
                "stock_quantity": 42,
                "supplier_name": "Logitech Global Supply",
            },
            {
                "name": "Keychron K2 Mechanical Keyboard",
                "sku": "ELEC-KEY-002",
                "category": "Electronics",
                "description": "Wireless mechanical keyboard with Gateron Brown switches and RGB backlight.",
                "purchase_price": Decimal("55.00"),
                "selling_price": Decimal("89.00"),
                "stock_quantity": 6,  # LOW STOCK (< 10)
                "supplier_name": "Keychron Tech Ltd.",
            },
            {
                "name": "Sony WH-1000XM5 Noise Canceling Headphones",
                "sku": "ELEC-AUD-005",
                "category": "Electronics",
                "description": "Premium active noise canceling wireless over-ear headphones.",
                "purchase_price": Decimal("240.00"),
                "selling_price": Decimal("398.00"),
                "stock_quantity": 0,  # OUT OF STOCK (== 0)
                "supplier_name": "Apex Audio Wholesale",
            },
            {
                "name": "Anker 65W GaN USB-C Fast Charger",
                "sku": "ELEC-CHG-065",
                "category": "Electronics",
                "description": "Compact triple-port fast wall charger for laptops and mobile devices.",
                "purchase_price": Decimal("18.00"),
                "selling_price": Decimal("39.99"),
                "stock_quantity": 55,
                "supplier_name": "Anker Innovations",
            },
            {
                "name": "Herman Miller Aeron Ergonomic Chair",
                "sku": "FURN-CHR-001",
                "category": "Furniture",
                "description": "Adjustable posturefit lumbar support mesh executive desk chair.",
                "purchase_price": Decimal("750.00"),
                "selling_price": Decimal("1295.00"),
                "stock_quantity": 4,  # LOW STOCK (< 10)
                "supplier_name": "MillerKnoll Direct",
            },
            {
                "name": "Autonomous SmartDesk Pro (60x30)",
                "sku": "FURN-DSK-002",
                "category": "Furniture",
                "description": "Dual-motor motorized standing desk with solid oak desktop finish.",
                "purchase_price": Decimal("320.00"),
                "selling_price": Decimal("549.00"),
                "stock_quantity": 11,
                "supplier_name": "Autonomous Inc.",
            },
            {
                "name": "Heavy Duty Steel Filing Cabinet 3-Drawer",
                "sku": "FURN-CAB-003",
                "category": "Furniture",
                "description": "Lockable anti-tilt filing cabinet with legal and letter size hanging folder support.",
                "purchase_price": Decimal("110.00"),
                "selling_price": Decimal("185.00"),
                "stock_quantity": 0,  # OUT OF STOCK (== 0)
                "supplier_name": "Commercial Office Supplies",
            },
            {
                "name": "Premium Multi-Purpose A4 Copy Paper (Case)",
                "sku": "OFFC-PAP-500",
                "category": "Office Supplies",
                "description": "Box of 10 reams, 5000 sheets total, 80gsm bright white paper.",
                "purchase_price": Decimal("28.00"),
                "selling_price": Decimal("44.50"),
                "stock_quantity": 88,
                "supplier_name": "International Paper Co.",
            },
            {
                "name": "Pilot G2 Gel Roller Pens (Pack of 12)",
                "sku": "OFFC-PEN-012",
                "category": "Office Supplies",
                "description": "Smooth writing 0.7mm fine point black refillable gel ink pens.",
                "purchase_price": Decimal("7.20"),
                "selling_price": Decimal("14.99"),
                "stock_quantity": 7,  # LOW STOCK (< 10)
                "supplier_name": "Pilot Pen Corp",
            },
            {
                "name": "UniFi 24-Port PoE Gigabit Switch",
                "sku": "NET-SWI-024",
                "category": "Networking & IT",
                "description": "Managed Layer 2 PoE switch with auto-sensing IEEE 802.3af/at ports and SFP uplink.",
                "purchase_price": Decimal("260.00"),
                "selling_price": Decimal("399.00"),
                "stock_quantity": 8,  # LOW STOCK (< 10)
                "supplier_name": "Ubiquiti Networks Reseller",
            },
            {
                "name": "Cat6 Shielded Ethernet Cable (1000ft Spool)",
                "sku": "NET-CAB-100",
                "category": "Networking & IT",
                "description": "Pure solid copper bulk Ethernet wire for Gigabit enterprise installations.",
                "purchase_price": Decimal("95.00"),
                "selling_price": Decimal("165.00"),
                "stock_quantity": 18,
                "supplier_name": "CableMatters Wholesaler",
            },
            {
                "name": "Nespresso VertuoPlus Commercial Coffee Machine",
                "sku": "PAN-COF-001",
                "category": "Breakroom & Pantry",
                "description": "Single-serve commercial coffee & espresso maker with centrifusion extraction technology.",
                "purchase_price": Decimal("115.00"),
                "selling_price": Decimal("179.99"),
                "stock_quantity": 14,
                "supplier_name": "Nespresso Business Solutions",
            },
            {
                "name": "Nespresso Espresso Roast Capsules (Box of 50)",
                "sku": "PAN-CAP-050",
                "category": "Breakroom & Pantry",
                "description": "Dark roast intense Italian blend recyclable aluminum capsules.",
                "purchase_price": Decimal("25.00"),
                "selling_price": Decimal("42.00"),
                "stock_quantity": 2,  # LOW STOCK (< 10)
                "supplier_name": "Nespresso Business Solutions",
            },
            {
                "name": "Eco-Friendly Compostable Paper Cups (500 count)",
                "sku": "PAN-CUP-500",
                "category": "Breakroom & Pantry",
                "description": "Double wall insulated hot beverage coffee cups, 100% plant fiber.",
                "purchase_price": Decimal("22.00"),
                "selling_price": Decimal("38.50"),
                "stock_quantity": 0,  # OUT OF STOCK (== 0)
                "supplier_name": "GreenLife Supplies",
            },
        ]

        for item in products_data:
            cat = categories_map[item["category"]]
            prod, created = Product.objects.get_or_create(
                sku=item["sku"],
                defaults={
                    "name": item["name"],
                    "category": cat,
                    "description": item["description"],
                    "purchase_price": item["purchase_price"],
                    "selling_price": item["selling_price"],
                    "stock_quantity": item["stock_quantity"],
                    "supplier_name": item["supplier_name"],
                }
            )
            if created:
                self.stdout.write(f"  + Created Product: {prod.name} (Stock: {prod.stock_quantity})")

        # Create Default Superuser if not exists
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin123")
            self.stdout.write("  + Created default admin user: admin / admin123")

        self.stdout.write(self.style.SUCCESS("Successfully seeded sample categories and products!"))
