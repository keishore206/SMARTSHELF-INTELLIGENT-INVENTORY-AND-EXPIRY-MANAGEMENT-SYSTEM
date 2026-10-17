"""
inventory_logic.py  -  SmartShelf
Business rules for expiry status and low-stock detection.
Pure functions; no Streamlit or database imports here.
"""

from datetime import date, datetime

# Default warning window (days before expiry to raise an alert)
EXPIRY_WARNING_DAYS = 7


def parse_expiry(expiry_date_str):
    """Return a date object from an ISO-8601 string, or None if blank/invalid."""
    if not expiry_date_str:
        return None
    try:
        return datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


def get_expiry_status(expiry_date_str, today=None):
    """
    Return one of:
      'N/A'           - product has no expiry date
      'Expired'       - past expiry date
      'Expiring Soon' - within EXPIRY_WARNING_DAYS days
      'OK'            - beyond warning window
    """
    if today is None:
        today = date.today()
    exp = parse_expiry(expiry_date_str)
    if exp is None:
        return "N/A"
    delta = (exp - today).days
    if delta < 0:
        return "Expired"
    if delta <= EXPIRY_WARNING_DAYS:
        return "Expiring Soon"
    return "OK"


def days_until_expiry(expiry_date_str, today=None):
    """Return integer days until expiry, or None if no expiry date."""
    if today is None:
        today = date.today()
    exp = parse_expiry(expiry_date_str)
    if exp is None:
        return None
    return (exp - today).days


def get_stock_status(quantity, min_stock):
    """Return 'Out of Stock', 'Low Stock', or 'In Stock'."""
    if quantity == 0:
        return "Out of Stock"
    if quantity <= min_stock:
        return "Low Stock"
    return "In Stock"


def enrich_products(products, today=None):
    """
    Add computed fields to each product dict:
      expiry_status, days_until_expiry, stock_status
    """
    if today is None:
        today = date.today()
    enriched = []
    for p in products:
        row = dict(p)
        row["expiry_status"] = get_expiry_status(row.get("expiry_date"), today)
        row["days_until_expiry"] = days_until_expiry(row.get("expiry_date"), today)
        row["stock_status"] = get_stock_status(row.get("quantity", 0), row.get("min_stock", 5))
        enriched.append(row)
    return enriched


def filter_expired(products):
    return [p for p in products if p.get("expiry_status") == "Expired"]


def filter_expiring_soon(products):
    return [p for p in products if p.get("expiry_status") == "Expiring Soon"]


def filter_low_stock(products):
    return [p for p in products if p.get("stock_status") in ("Low Stock", "Out of Stock")]


def dashboard_counts(products):
    """Return a dict of counts used by the dashboard."""
    return {
        "total": len(products),
        "expired": len(filter_expired(products)),
        "expiring_soon": len(filter_expiring_soon(products)),
        "low_stock": len(filter_low_stock(products)),
        "out_of_stock": len([p for p in products if p.get("stock_status") == "Out of Stock"]),
    }
