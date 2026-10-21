"""
SmartShelf Enterprise Platform - Unified Main Application
Backend: FastAPI (Python)
Database: SQLite (smartshelf/data/smartshelf.db)
Main Frontend: Google Stitch Enterprise Suite
Backup Interface: Streamlit Analytics Studio
"""

import sys
import os
import datetime
import subprocess
import threading
import time
import socket
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response, JSONResponse
from pydantic import BaseModel, Field

# Ensure smartshelf directory is in python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SMARTSHELF_DIR = os.path.join(PROJECT_ROOT, "smartshelf")
STATIC_DIR = os.path.join(PROJECT_ROOT, "stitch_smartshelf_enterprise_inventory_suite")

if SMARTSHELF_DIR not in sys.path:
    sys.path.insert(0, SMARTSHELF_DIR)

import database as db
import inventory_logic as logic
import reports

# Initialize FastAPI App with metadata for Swagger UI docs
app = FastAPI(
    title="SmartShelf Enterprise API",
    description="Intelligent Inventory Monitoring & Automated Expiry Alert System API",
    version="1.2.0 Enterprise",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for cross-origin integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================= DATA SEEDING & DATABASE INIT =================
def ensure_db_seeded():
    """Ensure database schema is created and demo data is populated if empty."""
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


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0


def ensure_streamlit_running():
    """Starts Streamlit as a managed background service if not already active on 8501."""
    if not is_port_in_use(8501):
        def _run():
            try:
                subprocess.Popen(
                    [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501", "--server.headless", "true"],
                    cwd=SMARTSHELF_DIR,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except Exception as e:
                print(f"[Warning] Could not auto-launch Streamlit: {e}")

        t = threading.Thread(target=_run, daemon=True)
        t.start()


# ================= PYDANTIC SCHEMAS =================
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Product Name")
    category: str = Field(..., min_length=1, description="Product Category")
    quantity: int = Field(0, ge=0, description="Available stock quantity")
    unit_price: float = Field(0.0, ge=0.0, description="Price per unit in Rs")
    expiry_date: Optional[str] = Field(None, description="Expiry date in ISO format YYYY-MM-DD")
    min_stock: int = Field(5, ge=0, description="Minimum alert threshold")


class ProductUpdate(BaseModel):
    name: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=0)
    unit_price: float = Field(..., ge=0.0)
    expiry_date: Optional[str] = None
    min_stock: int = Field(..., ge=0)


# ================= REST API ENDPOINTS =================
@app.get("/api/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "SmartShelf Enterprise",
        "timestamp": datetime.datetime.now().isoformat(),
        "database": "SQLite (Connected)",
        "streamlit_backup_port": 8501
    }


@app.get("/api/stats", tags=["Analytics"])
def get_dashboard_stats():
    raw_products = db.get_all_products()
    products = logic.enrich_products(raw_products)
    counts = logic.dashboard_counts(products)
    stats = db.get_dashboard_stats()

    # Calculate category units & distribution
    cat_map = {}
    for p in products:
        cat = p.get("category", "General")
        cat_map[cat] = cat_map.get(cat, 0) + p.get("quantity", 0)

    total_units = stats["total_units"] or 1
    sorted_cats = sorted(cat_map.items(), key=lambda x: x[1], reverse=True)
    cat_list = [
        {"name": name, "units": units, "pct": round((units / total_units) * 100, 1)}
        for name, units in sorted_cats
    ]

    return {
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


@app.get("/api/products", tags=["Inventory"])
def list_products(
    q: Optional[str] = Query(None, description="Search query across name and ID"),
    category: Optional[str] = Query("All", description="Filter by category"),
    stock_status: Optional[str] = Query("All", description="Filter by stock status"),
    expiry_status: Optional[str] = Query("All", description="Filter by expiry status")
):
    raw_products = db.get_all_products()
    products = logic.enrich_products(raw_products)

    filtered = []
    q_clean = (q or "").lower().strip()
    for p in products:
        if q_clean and (q_clean not in p["name"].lower() and str(p["id"]) != q_clean and f"sku-{p['id']}".lower() != q_clean):
            continue
        if category and category != "All" and p["category"] != category:
            continue
        if stock_status and stock_status != "All" and p["stock_status"] != stock_status:
            continue
        if expiry_status and expiry_status != "All" and p["expiry_status"] != expiry_status:
            continue
        filtered.append(p)

    return filtered


@app.get("/api/products/{product_id}", tags=["Inventory"])
def get_product(product_id: int):
    p = db.get_product_by_id(product_id)
    if not p:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
    return logic.enrich_products([p])[0]


@app.post("/api/products", status_code=status.HTTP_201_CREATED, tags=["Inventory"])
def create_product(product: ProductCreate):
    pid = db.add_product(
        name=product.name,
        category=product.category,
        quantity=product.quantity,
        unit_price=product.unit_price,
        expiry_date=product.expiry_date,
        min_stock=product.min_stock
    )
    created = db.get_product_by_id(pid)
    return logic.enrich_products([created])[0]


@app.put("/api/products/{product_id}", tags=["Inventory"])
def update_product(product_id: int, product: ProductUpdate):
    ok = db.update_product(
        product_id=product_id,
        name=product.name,
        category=product.category,
        quantity=product.quantity,
        unit_price=product.unit_price,
        expiry_date=product.expiry_date,
        min_stock=product.min_stock
    )
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found or update failed")
    updated = db.get_product_by_id(product_id)
    return logic.enrich_products([updated])[0]


@app.delete("/api/products/{product_id}", tags=["Inventory"])
def delete_product(product_id: int):
    ok = db.delete_product(product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"success": True, "deleted_id": product_id}


@app.get("/api/alerts", tags=["Monitoring"])
def get_alerts():
    products = logic.enrich_products(db.get_all_products())
    expired = logic.filter_expired(products)
    expiring_soon = logic.filter_expiring_soon(products)
    low_stock = [p for p in products if p.get("stock_status") == "Low Stock"]
    out_of_stock = [p for p in products if p.get("stock_status") == "Out of Stock"]
    expired_value = sum(p.get("quantity", 0) * p.get("unit_price", 0) for p in expired)

    return {
        "expired": expired,
        "expiring_soon": expiring_soon,
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "expired_value": expired_value,
        "total_alerts": len(expired) + len(expiring_soon) + len(low_stock) + len(out_of_stock),
    }


@app.get("/api/audit-log", tags=["Governance"])
def get_audit_log(limit: int = 100):
    return db.get_audit_log(limit=limit)


@app.get("/api/export/csv", tags=["Reports"])
def export_csv():
    products = logic.enrich_products(db.get_all_products())
    csv_bytes = reports.products_to_csv(products)
    return Response(
        content=csv_bytes,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="smartshelf_inventory.csv"'}
    )


@app.get("/api/export/summary", tags=["Reports"])
def export_summary():
    products = logic.enrich_products(db.get_all_products())
    summary_txt = reports.build_summary(products).encode("utf-8")
    return Response(
        content=summary_txt,
        media_type="text/plain; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="smartshelf_summary.txt"'}
    )


@app.post("/api/seed", tags=["System"])
def seed_database():
    ensure_db_seeded()
    return {"message": "Database successfully seeded with demo products!"}


# ================= FRONTEND MOUNT & SERVING =================
# Serve root index.html from Stitch UI suite
@app.get("/", tags=["UI"])
def serve_stitch_ui():
    root_index = os.path.join(PROJECT_ROOT, "index.html")
    if os.path.exists(root_index):
        return FileResponse(root_index)
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    raise HTTPException(status_code=404, detail="Stitch UI index.html not found")


# Mount static assets directory
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ================= LIFECYCLE & SERVER RUNNER =================
@app.on_event("startup")
def on_startup():
    ensure_db_seeded()
    ensure_streamlit_running()
    print("================================================================")
    print("  SmartShelf Enterprise Platform (FastAPI + Stitch UI)")
    print("  Main Application (Stitch UI): http://localhost:5000")
    print("  Interactive API Documentation: http://localhost:5000/docs")
    print("  Streamlit Analytics Backup:    http://localhost:8501")
    print("================================================================")


if __name__ == "__main__":
    import uvicorn
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
