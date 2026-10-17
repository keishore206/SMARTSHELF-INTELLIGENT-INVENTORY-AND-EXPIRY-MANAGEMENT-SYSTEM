"""
reports.py  -  SmartShelf
CSV export and summary report preparation.
"""

import io
import csv
from datetime import date

from inventory_logic import enrich_products


EXPORT_COLUMNS = [
    "id", "name", "category", "quantity", "unit_price",
    "expiry_date", "min_stock", "stock_status", "expiry_status",
    "days_until_expiry", "created_at", "updated_at",
]


def products_to_csv(products):
    """
    Return a UTF-8 CSV string for the given enriched products list.
    The caller is responsible for passing already-enriched products,
    or raw products (will be enriched here).
    """
    if products and "stock_status" not in products[0]:
        products = enrich_products(products)

    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=EXPORT_COLUMNS,
        extrasaction="ignore",
        lineterminator="\r\n",
    )
    writer.writeheader()
    for row in products:
        writer.writerow(row)
    return output.getvalue().encode("utf-8")


def build_summary(products):
    """Return a simple text summary string for the current inventory."""
    if products and "stock_status" not in products[0]:
        products = enrich_products(products)

    today = date.today().isoformat()
    total = len(products)
    total_units = sum(p.get("quantity", 0) for p in products)
    total_value = sum(p.get("quantity", 0) * p.get("unit_price", 0) for p in products)
    expired = sum(1 for p in products if p.get("expiry_status") == "Expired")
    expiring_soon = sum(1 for p in products if p.get("expiry_status") == "Expiring Soon")
    low_stock = sum(1 for p in products if p.get("stock_status") in ("Low Stock", "Out of Stock"))

    lines = [
        f"SmartShelf Inventory Summary  |  Generated: {today}",
        "=" * 55,
        f"Total products     : {total}",
        f"Total units        : {total_units}",
        f"Total stock value  : Rs {total_value:,.2f}",
        f"Expired items      : {expired}",
        f"Expiring soon      : {expiring_soon}",
        f"Low / out of stock : {low_stock}",
    ]
    return "\n".join(lines)
