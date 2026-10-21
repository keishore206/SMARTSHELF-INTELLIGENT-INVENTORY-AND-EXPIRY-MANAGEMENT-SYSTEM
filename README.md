# SMARTSHELF — Intelligent Inventory and Expiry Management System

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-4285F4?style=for-the-badge&logo=github&logoColor=white)](https://keishore206.github.io/SMARTSHELF-INTELLIGENT-INVENTORY-AND-EXPIRY-MANAGEMENT-SYSTEM/)
[![Python 3.11](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-WAL%20Mode-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Stitch UI](https://img.shields.io/badge/Google%20Stitch-Enterprise%20UI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://stitch.withgoogle.com/)
[![Pytest](https://img.shields.io/badge/Pytest-Passing%20(9%2F9)-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)

---

## 🌐 Live Hosted Web Application (GitHub Pages)

Experience the complete enterprise inventory and expiry platform live in your browser — zero installation or setup required:

👉 **[https://keishore206.github.io/SMARTSHELF-INTELLIGENT-INVENTORY-AND-EXPIRY-MANAGEMENT-SYSTEM/](https://keishore206.github.io/SMARTSHELF-INTELLIGENT-INVENTORY-AND-EXPIRY-MANAGEMENT-SYSTEM/)**

| Capability | Cloud Hosted Mode (GitHub Pages) | Local Enterprise Server (`python main.py`) |
| :--- | :--- | :--- |
| **Deployment / Access** | Publicly accessible URL on GitHub Pages | Localhost ASGI server on Port 5000 |
| **Data Engine** | Browser Reactive Persistence (`localStorage`) | ACID SQLite WAL Database (`smartshelf.db`) |
| **Executive Dashboard & KPIs** | ✅ Real-time valuation, shelf health, categories | ✅ Real-time valuation, shelf health, categories |
| **Catalog Inspector & Drawer** | ✅ Multi-matrix search, filters, and SKU drawer | ✅ Multi-matrix search, filters, and SKU drawer |
| **Product Lifecycle (Add/Edit/Delete)** | ✅ Fully functional client-side CRUD | ✅ Parameterised SQL CRUD with CHECK rules |
| **Expiration Exception Alerts** | ✅ Deterministic expiration horizon engine | ✅ Deterministic expiration horizon engine |
| **Reports Center (CSV & TXT)** | ✅ Instant in-browser Blob file downloads | ✅ FastAPI streaming endpoint file downloads |
| **System Governance Audit Log** | ✅ Chronological log with JSON export | ✅ Immutable SQLite audit table + JSON export |
| **Streamlit Analytics Studio** | 💡 Embedded architecture notice & preview | ✅ Native Python Streamlit runtime (Port 8501) |

---

## 📌 Project Overview

**SmartShelf** is a unified, enterprise-grade inventory and expiry management platform engineered to eliminate retail food waste, reduce stockouts, and enforce regulatory compliance. It replaces manual spreadsheets and paper ledgers with automated expiration horizon tracking, safety stock reorder alerts, parameterised transactional persistence, and an immutable audit governance ledger.

The platform unites a **Google Stitch single-page application (SPA)** on the frontend with a high-performance **Python FastAPI backend**, an **SQLite database (WAL mode)**, and an integrated **Streamlit Analytics Studio**.

---

## 🏗️ System Architecture

SmartShelf operates as a decoupled 3-tier architecture with an integrated secondary analytics runtime:

```
[ User Browser / Desktop Client ]
              │
              ▼ (HTTP / JSON REST)
┌────────────────────────────────────────────────────────┐
│             PRESENTATION LAYER (PORT 5000)             │
│   Google Stitch Enterprise UI Suite (SPA)              │
│   • Executive Inventory Dashboard                      │
│   • Inventory Catalog Inspector & Drawer               │
│   • Register New Product Form with Real-Time Valuation │
│   • Edit Product & Lifecycle Manager                   │
│   • Alerts & Expiration Exception Hub                  │
│   • Reports & Data Export Center (CSV / JSON)          │
│   • System Audit Log & Governance Ledger               │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼ (FastAPI Router)
┌────────────────────────────────────────────────────────┐
│             APPLICATION LAYER (UVICORN ASGI)           │
│   Python 3.11 + FastAPI REST Backend                   │
│   • Parameterised Pydantic Request Validation          │
│   • Deterministic Expiry & Low-Stock Rules Engine      │
│   • OpenAPI Swagger Interactive Documentation (/docs)  │
│   • Embedded Streamlit Studio Proxy (Port 8501)        │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼ (SQL with '?' Placeholders)
┌────────────────────────────────────────────────────────┐
│               DATABASE LAYER (SQLITE 3)                │
│   smartshelf/data/smartshelf.db                        │
│   • ACID-Compliant Transactional Engine                │
│   • Write-Ahead Logging (WAL) Mode Concurrency         │
│   • Products Schema with CHECK Constraints             │
│   • Immutable Audit Trails (ADD, EDIT, DELETE)         │
└────────────────────────────────────────────────────────┘
```

---

## 🚀 Quickstart & How to Run

### Method 0: Instant Access via GitHub Pages (Zero Installation)
Launch the cloud version instantly in any web browser without cloning or installing dependencies:
👉 **[Open SmartShelf on GitHub Pages](https://keishore206.github.io/SMARTSHELF-INTELLIGENT-INVENTORY-AND-EXPIRY-MANAGEMENT-SYSTEM/)**

---

### Method 1: One-Click Windows Launcher (Recommended for Full Local Stack)
Double-click the included batch launcher:
```bat
run_enterprise.bat
```
This automatically initializes the SQLite database, launches the FastAPI server, and opens the application at `http://localhost:5000`.

### Method 2: Command Line (PowerShell / Terminal)
```bash
# 1. Clone the repository
git clone https://github.com/keishore206/SMARTSHELF-INTELLIGENT-INVENTORY-AND-EXPIRY-MANAGEMENT-SYSTEM.git
cd SMARTSHELF-INTELLIGENT-INVENTORY-AND-EXPIRY-MANAGEMENT-SYSTEM

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the unified platform on port 5000
python main.py 5000
```
- **Main Application**: [http://localhost:5000](http://localhost:5000)
- **Interactive API Documentation (Swagger)**: [http://localhost:5000/docs](http://localhost:5000/docs)
- **Secondary Streamlit Studio**: [http://localhost:8501](http://localhost:8501) (or embedded via Stitch UI navigation)

### Method 3: NPM Start
```bash
npm start
```

---

## 📊 Core Modules & Capabilities

### Module 1: Data Engineering
- **Schema Management**: Relational `products` table tracking `product_id`, `product_name`, `category`, `quantity`, `price`, `expiry_date`, and `min_stock`.
- **Dynamic Valuation**: Real-time batch asset value computation (`Quantity × Unit Price`).
- **Catalog Inspector**: Multi-filter matrix (Keyword Search, Category Filter, Expiration Lifecycle, Stock Threshold) with a right-hand profile drawer.

### Module 2: Cloud Engineering
- **High-Throughput ASGI**: Powered by Starlette & Uvicorn for asynchronous I/O.
- **OpenAPI 3.0 Contract**: Interactive Swagger UI at `/docs` and ReDoc at `/redoc`.
- **Stateless REST Handlers**: Clean routing architecture ready for cloud deployment (Docker, Render, AWS, or Streamlit Cloud).

### Module 3: AI & Inventory Intelligence
- **Deterministic Rules Engine**:
  - `Expired`: $\text{Expiry Date} < \text{Current Date}$ (Triggers write-off valuation alert).
  - `Near Expiry`: $\text{Current Date} \le \text{Expiry Date} \le \text{Current Date} + 7\text{ days}$.
  - `Low Stock`: $\text{Stock Quantity} < \text{Safety Threshold}$.
  - `Safe`: Meets all shelf-life and buffer requirements.
- **Bento Risk Trio**: Real-time executive KPIs highlighting inventory at risk.

### Module 4: Security Engineering
- **SQL Injection Prevention**: 100% parameterised SQL statements (`?` bindings) across all CRUD operations.
- **Input Validation**: Strict constraints preventing negative stock counts, blank fields, and corrupted calendar dates.
- **Governance Ledger**: Immutable audit log recording every `ADD`, `EDIT`, and `DELETE` event with full timestamps.

---

## 🔌 REST API Endpoints

| HTTP Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Service health status and database connectivity |
| `GET` | `/api/products` | Retrieve all inventory products with calculated statuses |
| `POST` | `/api/products` | Ingest new product record with input validation |
| `GET` | `/api/products/{id}` | Retrieve specific product details and audit history |
| `PUT` | `/api/products/{id}` | Update existing product parameters and log audit trail |
| `DELETE` | `/api/products/{id}` | Safely remove product record and record deletion event |
| `GET` | `/api/alerts/summary` | Real-time Bento counts (Expired, Near Expiry, Low Stock) |
| `GET` | `/api/audit-logs` | Retrieve chronological governance audit ledger |

---

## 🧪 Automated Testing

Run the automated test suite verifying deterministic business logic:
```bash
pytest smartshelf/tests/test_inventory_logic.py -v
```
All **9 test cases pass** across status resolution, expiry boundary detection, low-stock threshold triggers, and input edge cases.

---

## 📁 Repository Directory Structure

```
├── main.py                                      # Unified FastAPI application entry point
├── server.py                                    # REST API router and route definitions
├── run_enterprise.bat                           # Windows one-click desktop launcher
├── requirements.txt                             # Python dependencies
├── package.json                                 # NPM automation scripts
├── HOW_TO_USE.docx                              # Enterprise user manual (Word format)
├── HOW_TO_USE.txt                               # Enterprise user manual (Text format)
├── SmartShelf_PRD.docx                          # Product Requirements Document
├── Project_Report/                              # Academic project documentation
│   └── CPPE_Mini_project_2_report_KEISHORE 345678.docx
├── diagrams/                                    # 5 publication-quality system diagrams
│   ├── fig_3_1_architecture.png
│   ├── fig_4_1_data_engineering.png
│   ├── fig_4_2_cloud_engineering.png
│   ├── fig_4_3_ai_engineering.png
│   └── fig_4_4_security_engineering.png
├── screenshots/                                 # High-resolution supplementary UI captures
│   ├── terminal_server_running.png
│   ├── swagger_api_docs.png
│   ├── validation_error_quantity.png
│   └── validation_error_missing_field.png
├── stitch_smartshelf_enterprise_inventory_suite/ # Primary Google Stitch SPA
│   ├── index.html                               # Responsive single-page application
│   ├── executive_inventory_dashboard/
│   ├── inventory_catalog_inspector/
│   ├── register_new_product_form/
│   ├── edit_product_lifecycle_manager/
│   ├── alerts_expiration_exception_hub/
│   ├── reports_data_export_center/
│   └── system_audit_log_governance_ledger/
└── smartshelf/                                  # Core Python package & Streamlit studio
    ├── app.py                                   # Streamlit multi-page interface
    ├── database.py                              # SQLite connection, WAL mode, migrations
    ├── inventory_logic.py                       # Pure business rules engine
    ├── data/                                    # Persistent SQLite database storage
    │   └── smartshelf.db
    ├── pages/                                   # Streamlit interface pages
    └── tests/                                   # Automated Pytest suite
```

---

## 📜 Academic Certification & Acknowledgements

This project was developed by **KEISHORE G** (`23UCS086`) as part of **Mini Project 2 (CPPE)** under the guidance of **Dr. M. SHANMUGAM**, Department of Computer Science and Engineering, **Sri Manakula Vinayagar Engineering College (Autonomous)**, Puducherry.
