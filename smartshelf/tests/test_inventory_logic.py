"""
tests/test_inventory_logic.py  -  SmartShelf
Unit tests for expiry and stock rules (pytest).
Run: pytest tests/ -v
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta
import inventory_logic as logic

TODAY = date(2026, 10, 15)


def _days(n):
    return (TODAY + timedelta(days=n)).isoformat()


def test_expired():
    assert logic.get_expiry_status(_days(-1), today=TODAY) == "Expired"
    assert logic.get_expiry_status(_days(-30), today=TODAY) == "Expired"


def test_expiring_soon():
    assert logic.get_expiry_status(_days(0), today=TODAY) == "Expiring Soon"
    assert logic.get_expiry_status(_days(7), today=TODAY) == "Expiring Soon"


def test_ok():
    assert logic.get_expiry_status(_days(8), today=TODAY) == "OK"
    assert logic.get_expiry_status(_days(30), today=TODAY) == "OK"


def test_no_expiry():
    assert logic.get_expiry_status(None, today=TODAY) == "N/A"
    assert logic.get_expiry_status("", today=TODAY) == "N/A"


def test_low_stock_at_threshold():
    assert logic.get_stock_status(5, 5) == "Low Stock"


def test_out_of_stock():
    assert logic.get_stock_status(0, 5) == "Out of Stock"


def test_in_stock():
    assert logic.get_stock_status(10, 5) == "In Stock"


def test_enrich():
    raw = [
        {"id": 1, "name": "Milk", "category": "Dairy", "quantity": 3,
         "unit_price": 32.0, "expiry_date": _days(-1), "min_stock": 5},
    ]
    enriched = logic.enrich_products(raw, today=TODAY)
    assert enriched[0]["expiry_status"] == "Expired"
    assert enriched[0]["stock_status"] == "Low Stock"
    assert enriched[0]["days_until_expiry"] == -1


def test_dashboard_counts():
    raw = [
        {"id": 1, "name": "A", "category": "X", "quantity": 0,
         "expiry_date": _days(-5), "min_stock": 5},
        {"id": 2, "name": "B", "category": "X", "quantity": 3,
         "expiry_date": _days(3), "min_stock": 5},
        {"id": 3, "name": "C", "category": "X", "quantity": 20,
         "expiry_date": _days(30), "min_stock": 5},
    ]
    enriched = logic.enrich_products(raw, today=TODAY)
    counts = logic.dashboard_counts(enriched)
    assert counts["total"] == 3
    assert counts["expired"] == 1
    assert counts["expiring_soon"] == 1
    assert counts["low_stock"] == 2
    assert counts["out_of_stock"] == 1
