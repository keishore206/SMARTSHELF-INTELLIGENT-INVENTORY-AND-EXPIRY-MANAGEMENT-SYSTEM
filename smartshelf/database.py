"""
database.py  -  SmartShelf
SQLite connection, schema initialisation, and all CRUD operations.
All queries use parameterised values to prevent SQL injection.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "smartshelf.db")


def get_connection():
    """Return a WAL-mode connection with row_factory for dict-like access."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """Create tables if they do not already exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                category    TEXT    NOT NULL,
                quantity    INTEGER NOT NULL CHECK(quantity >= 0),
                unit_price  REAL    NOT NULL CHECK(unit_price >= 0),
                expiry_date TEXT,
                min_stock   INTEGER NOT NULL DEFAULT 5 CHECK(min_stock >= 0),
                created_at  TEXT    NOT NULL,
                updated_at  TEXT    NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                action      TEXT    NOT NULL,
                product_id  INTEGER,
                details     TEXT,
                timestamp   TEXT    NOT NULL
            )
        """)
        conn.commit()


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _log(conn, action, product_id, details):
    conn.execute(
        "INSERT INTO audit_log (action, product_id, details, timestamp) VALUES (?,?,?,?)",
        (action, product_id, details, _now()),
    )


def add_product(name, category, quantity, unit_price, expiry_date, min_stock):
    """Insert a new product and return the new row id."""
    ts = _now()
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO products
               (name, category, quantity, unit_price, expiry_date, min_stock, created_at, updated_at)
               VALUES (?,?,?,?,?,?,?,?)""",
            (name.strip(), category.strip(), int(quantity), float(unit_price),
             expiry_date or None, int(min_stock), ts, ts),
        )
        pid = cur.lastrowid
        _log(conn, "ADD", pid, f"Added product '{name}'")
        conn.commit()
    return pid


def get_all_products():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM products ORDER BY name COLLATE NOCASE"
        ).fetchall()
    return [dict(r) for r in rows]


def get_product_by_id(product_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM products WHERE id=?", (product_id,)
        ).fetchone()
    return dict(row) if row else None


def search_products(query="", category=""):
    sql = "SELECT * FROM products WHERE 1=1"
    params = []
    if query.strip():
        sql += " AND name LIKE ?"
        params.append(f"%{query.strip()}%")
    if category.strip() and category != "All":
        sql += " AND category = ?"
        params.append(category.strip())
    sql += " ORDER BY name COLLATE NOCASE"
    with get_connection() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]


def get_categories():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT category FROM products ORDER BY category COLLATE NOCASE"
        ).fetchall()
    return [r[0] for r in rows]


def update_product(product_id, name, category, quantity, unit_price, expiry_date, min_stock):
    ts = _now()
    with get_connection() as conn:
        cur = conn.execute(
            """UPDATE products SET name=?,category=?,quantity=?,unit_price=?,
               expiry_date=?,min_stock=?,updated_at=? WHERE id=?""",
            (name.strip(), category.strip(), int(quantity), float(unit_price),
             expiry_date or None, int(min_stock), ts, product_id),
        )
        ok = cur.rowcount > 0
        if ok:
            _log(conn, "EDIT", product_id, f"Updated product '{name}'")
        conn.commit()
    return ok


def delete_product(product_id):
    product = get_product_by_id(product_id)
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM products WHERE id=?", (product_id,))
        ok = cur.rowcount > 0
        if ok and product:
            _log(conn, "DELETE", product_id, f"Deleted product '{product['name']}'")
        conn.commit()
    return ok


def get_audit_log(limit=50):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM audit_log ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_dashboard_stats():
    with get_connection() as conn:
        tp = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        tu = conn.execute("SELECT COALESCE(SUM(quantity),0) FROM products").fetchone()[0]
        tv = conn.execute(
            "SELECT COALESCE(SUM(quantity*unit_price),0) FROM products"
        ).fetchone()[0]
    return {"total_products": tp, "total_units": tu, "total_value": tv}
