"""
SmartShelf Enterprise Suite - Python Web & API Server
Connects the Google Stitch Enterprise UI to the SQLite database.
Pure Python standard library (http.server + sqlite3 + json).
"""

import sys
import os
import json
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime

# Ensure smartshelf directory is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SMARTSHELF_DIR = os.path.join(PROJECT_ROOT, "smartshelf")
STATIC_DIR = os.path.join(PROJECT_ROOT, "stitch_smartshelf_enterprise_inventory_suite")

if SMARTSHELF_DIR not in sys.path:
    sys.path.insert(0, SMARTSHELF_DIR)

import database as db
import inventory_logic as logic
import reports


def ensure_seeded():
    """Ensure database has initial enterprise data if empty."""
    db.init_db()
    products = db.get_all_products()
    if not products:
        today = datetime.date.today()
        seed_data = [
            {"name": "Whole Milk 1L", "category": "Dairy & Refrigerated", "quantity": 42, "unit_price": 32.0, "expiry_date": (today + datetime.timedelta(days=3)).strftime("%Y-%m-%d"), "min_stock": 15},
            {"name": "Artisan Baguette 400g", "category": "Bakery", "quantity": 18, "unit_price": 45.0, "expiry_date": (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d"), "min_stock": 10},
            {"name": "Fresh Greek Yogurt 500g", "category": "Dairy & Refrigerated", "quantity": 0, "unit_price": 85.0, "expiry_date": (today - datetime.timedelta(days=3)).strftime("%Y-%m-%d"), "min_stock": 10},
            {"name": "Cold Pressed Orange Juice 350ml", "category": "Beverages", "quantity": 8, "unit_price": 65.0, "expiry_date": (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d"), "min_stock": 15},
            {"name": "Cold Brew Coffee 330ml", "category": "Beverages", "quantity": 120, "unit_price": 85.0, "expiry_date": "2027-01-15", "min_stock": 20},
            {"name": "Baby Spinach 200g", "category": "Produce", "quantity": 14, "unit_price": 45.0, "expiry_date": (today + datetime.timedelta(days=2)).strftime("%Y-%m-%d"), "min_stock": 20},
            {"name": "Organic Basmati Rice 1kg", "category": "Grocery", "quantity": 25, "unit_price": 70.0, "expiry_date": "2027-04-01", "min_stock": 5},
            {"name": "Dishwashing Liquid Citrus 750ml", "category": "Household", "quantity": 32, "unit_price": 95.0, "expiry_date": None, "min_stock": 10},
            {"name": "Arabica Roast Coffee Beans 500g", "category": "Beverages", "quantity": 65, "unit_price": 350.0, "expiry_date": "2027-05-15", "min_stock": 15},
            {"name": "Almond Milk Unsweetened 1L", "category": "Dairy & Refrigerated", "quantity": 5, "unit_price": 110.0, "expiry_date": (today + datetime.timedelta(days=5)).strftime("%Y-%m-%d"), "min_stock": 10},
            {"name": "Sourdough Artisan Loaf", "category": "Bakery", "quantity": 3, "unit_price": 60.0, "expiry_date": (today - datetime.timedelta(days=2)).strftime("%Y-%m-%d"), "min_stock": 5},
            {"name": "Organic Haas Avocados 4pk", "category": "Produce", "quantity": 45, "unit_price": 120.0, "expiry_date": (today + datetime.timedelta(days=5)).strftime("%Y-%m-%d"), "min_stock": 10},
        ]
        for p in seed_data:
            db.add_product(p["name"], p["category"], p["quantity"], p["unit_price"], p["expiry_date"], p["min_stock"])


class SmartShelfRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def _send_json(self, data, status=200):
        body = json.dumps(data, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # API Endpoints
        if path == "/api/stats":
            products = logic.enrich_products(db.get_all_products())
            counts = logic.dashboard_counts(products)
            stats = db.get_dashboard_stats()
            
            # Category breakdown
            cat_map = {}
            for p in products:
                cat = p.get("category", "General")
                cat_map[cat] = cat_map.get(cat, 0) + p.get("quantity", 0)

            # Sort categories by units descending
            sorted_cats = sorted(cat_map.items(), key=lambda x: x[1], reverse=True)
            total_units = stats["total_units"] or 1
            cat_list = [
                {"name": name, "units": units, "pct": round((units / total_units) * 100, 1)}
                for name, units in sorted_cats
            ]

            data = {
                "total_products": stats["total_products"],
                "total_units": stats["total_units"],
                "total_value": stats["total_value"],
                "expired_count": counts["expired"],
                "expiring_soon_count": counts["expiring_soon"],
                "low_stock_count": counts["low_stock"],
                "out_of_stock_count": counts["out_of_stock"],
                "in_stock_count": stats["total_products"] - counts["low_stock"],
                "categories": cat_list,
            }
            return self._send_json(data)

        elif path == "/api/products":
            raw_products = db.get_all_products()
            products = logic.enrich_products(raw_products)

            # Apply filters if present
            q = query.get("q", [""])[0].lower().strip()
            cat = query.get("category", ["All"])[0].strip()
            stock_filter = query.get("stock_status", ["All"])[0].strip()
            expiry_filter = query.get("expiry_status", ["All"])[0].strip()

            filtered = []
            for p in products:
                if q and (q not in p["name"].lower() and str(p["id"]) != q and f"sku-{p['id']}".lower() != q):
                    continue
                if cat != "All" and p["category"] != cat:
                    continue
                if stock_filter != "All" and p["stock_status"] != stock_filter:
                    continue
                if expiry_filter != "All" and p["expiry_status"] != expiry_filter:
                    continue
                filtered.append(p)

            return self._send_json(filtered)

        elif path.startswith("/api/products/"):
            try:
                pid = int(path.split("/")[-1])
                p = db.get_product_by_id(pid)
                if not p:
                    return self._send_json({"error": "Product not found"}, 404)
                enriched = logic.enrich_products([p])[0]
                return self._send_json(enriched)
            except ValueError:
                return self._send_json({"error": "Invalid product ID"}, 400)

        elif path == "/api/alerts":
            products = logic.enrich_products(db.get_all_products())
            expired = logic.filter_expired(products)
            expiring_soon = logic.filter_expiring_soon(products)
            low_stock = [p for p in products if p.get("stock_status") == "Low Stock"]
            out_of_stock = [p for p in products if p.get("stock_status") == "Out of Stock"]
            expired_value = sum(p.get("quantity", 0) * p.get("unit_price", 0) for p in expired)

            return self._send_json({
                "expired": expired,
                "expiring_soon": expiring_soon,
                "low_stock": low_stock,
                "out_of_stock": out_of_stock,
                "expired_value": expired_value,
                "total_alerts": len(expired) + len(expiring_soon) + len(low_stock) + len(out_of_stock),
            })

        elif path == "/api/audit-log":
            logs = db.get_audit_log(limit=100)
            return self._send_json(logs)

        elif path == "/api/export/csv":
            products = logic.enrich_products(db.get_all_products())
            csv_bytes = reports.products_to_csv(products)
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Disposition", 'attachment; filename="smartshelf_inventory.csv"')
            self.send_header("Content-Length", str(len(csv_bytes)))
            self.end_headers()
            self.wfile.write(csv_bytes)
            return

        elif path == "/api/export/summary":
            products = logic.enrich_products(db.get_all_products())
            summary_txt = reports.build_summary(products).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Disposition", 'attachment; filename="smartshelf_summary.txt"')
            self.send_header("Content-Length", str(len(summary_txt)))
            self.end_headers()
            self.wfile.write(summary_txt)
            return

        # Serve default index.html for root or path
        if path == "/" or path == "":
            self.path = "/index.html"

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            body = json.loads(raw_body)
        except Exception:
            body = {}

        if path == "/api/products":
            name = body.get("name", "").strip()
            category = body.get("category", "").strip()
            quantity = int(body.get("quantity", 0))
            unit_price = float(body.get("unit_price", 0.0))
            expiry_date = body.get("expiry_date") or None
            min_stock = int(body.get("min_stock", 5))

            if not name or not category:
                return self._send_json({"error": "Product name and category are required"}, 400)
            if quantity < 0 or unit_price < 0 or min_stock < 0:
                return self._send_json({"error": "Numeric values cannot be negative"}, 400)

            pid = db.add_product(name, category, quantity, unit_price, expiry_date, min_stock)
            created = db.get_product_by_id(pid)
            return self._send_json(logic.enrich_products([created])[0], 201)

        elif path == "/api/seed":
            ensure_seeded()
            return self._send_json({"message": "Database seeded successfully!"})

        return self._send_json({"error": "Not found"}, 404)

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/products/"):
            try:
                pid = int(path.split("/")[-1])
            except ValueError:
                return self._send_json({"error": "Invalid product ID"}, 400)

            length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            try:
                body = json.loads(raw_body)
            except Exception:
                body = {}

            name = body.get("name", "").strip()
            category = body.get("category", "").strip()
            quantity = int(body.get("quantity", 0))
            unit_price = float(body.get("unit_price", 0.0))
            expiry_date = body.get("expiry_date") or None
            min_stock = int(body.get("min_stock", 5))

            if not name or not category:
                return self._send_json({"error": "Name and category are required"}, 400)

            ok = db.update_product(pid, name, category, quantity, unit_price, expiry_date, min_stock)
            if not ok:
                return self._send_json({"error": "Product not found or update failed"}, 404)

            updated = db.get_product_by_id(pid)
            return self._send_json(logic.enrich_products([updated])[0])

        return self._send_json({"error": "Not found"}, 404)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/products/"):
            try:
                pid = int(path.split("/")[-1])
            except ValueError:
                return self._send_json({"error": "Invalid product ID"}, 400)

            ok = db.delete_product(pid)
            if not ok:
                return self._send_json({"error": "Product not found"}, 404)

            return self._send_json({"success": True, "deleted_id": pid})

        return self._send_json({"error": "Not found"}, 404)


def run_server(port=5000):
    ensure_seeded()
    server_address = ("", port)
    httpd = HTTPServer(server_address, SmartShelfRequestHandler)
    print(f"================================================================")
    print(f"  SmartShelf Enterprise Platform Server Started Successfully!")
    print(f"  UI URL: http://localhost:{port}")
    print(f"  API:    http://localhost:{port}/api/products")
    print(f"================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down SmartShelf Enterprise server...")
        httpd.server_close()


if __name__ == "__main__":
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
