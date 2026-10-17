# SmartShelf
**Intelligent Inventory Monitoring and Automated Expiry Alert System**

> Wipro CPPE Mini Project | Python + Streamlit + SQLite

---

## Features
| # | Feature | Status |
|---|---------|--------|
| FR-01 | Dashboard with KPI metrics and charts | Must |
| FR-02 | Add product with validation | Must |
| FR-03 | View & search inventory | Must |
| FR-04 | Edit product | Must |
| FR-05 | Delete product (with confirmation) | Must |
| FR-06 | Expiry monitoring (Expired / Expiring Soon / OK) | Must |
| FR-07 | Low-stock alerts | Must |
| FR-08 | CSV export | Must |
| FR-09 | Charts (category & stock-status breakdown) | Should |
| FR-12 | Audit history log | Could |

---

## Project Structure

```
smartshelf/
├── app.py               # Streamlit entry point
├── database.py          # SQLite connection and CRUD operations
├── inventory_logic.py   # Expiry and low-stock business rules
├── reports.py           # CSV export and text summary
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── data/
│   └── smartshelf.db    # Auto-created SQLite database
└── tests/
    └── test_inventory_logic.py
```

---

## Setup

### Prerequisites
- Python 3.10 or later

### 1. Clone / copy this folder
```
cd smartshelf
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
streamlit run app.py
```

The app opens automatically at **http://localhost:8501**.

---

## Running Tests
```bash
pytest tests/ -v
```

---

## Expiry Rules
| Status | Condition |
|--------|-----------|
| **Expired** | Expiry date is before today |
| **Expiring Soon** | Expiry date is within 7 days |
| **OK** | Expiry date is more than 7 days away |
| **N/A** | Product has no expiry date |

## Stock Rules
| Status | Condition |
|--------|-----------|
| **Out of Stock** | Quantity = 0 |
| **Low Stock** | 0 < Quantity ≤ Minimum threshold |
| **In Stock** | Quantity > Minimum threshold |

---

## Demo Data (Appendix A from PRD)
| Product | Category | Qty | Price | Expiry |
|---------|----------|-----|-------|--------|
| Milk 500 ml | Dairy | 8 | 32.00 | 2026-10-18 |
| Bread | Bakery | 3 | 40.00 | 2026-10-16 |
| Rice 1 kg | Grocery | 25 | 70.00 | 2027-04-01 |
| Yogurt Cup | Dairy | 0 | 20.00 | 2026-10-14 |
| Dishwashing Liquid | Household | 2 | 95.00 | N/A |

---

## Security Notes
- All SQL queries are parameterised (no string interpolation).
- Database path uses an absolute path; do **not** commit `data/smartshelf.db` with real data.
- For multi-user deployment add authentication and restrict write actions.

---

*SmartShelf v1.0 | October 2026*
