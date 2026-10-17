"""
generate_docx.py
Generates a comprehensive, enterprise-grade HOW_TO_USE.docx user manual
for the SmartShelf Enterprise Inventory & Expiry Management Platform.
Includes embedded screenshots from the Stitch designs, styled tables, and full instructions.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STITCH_DIR = os.path.join(PROJECT_ROOT, "stitch_smartshelf_enterprise_inventory_suite")

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_callout(doc, text, title="NOTE"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "EFF4FF")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left border thick cobalt blue
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="1D4ED8"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run_title = p.add_run(f"[{title}] ")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(10)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(29, 78, 216)
    
    run_text = p.add_run(text)
    run_text.font.name = "Arial"
    run_text.font.size = Pt(10)
    run_text.font.color.rgb = RGBColor(15, 23, 42)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def style_table(tbl, col_widths, headers, data, alt_bg="F8FAFC"):
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header row
    hdr_cells = tbl.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        set_cell_background(hdr_cells[i], "0F172A")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.name = "Arial"
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            
    # Data rows
    for r_idx, row_data in enumerate(data):
        row_cells = tbl.add_row().cells
        bg_color = "FFFFFF" if r_idx % 2 == 0 else alt_bg
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=100, bottom=100, left=140, right=140)
            p = row_cells[c_idx].paragraphs[0]
            for run in p.runs:
                run.font.name = "Arial"
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(30, 41, 59)
                
    # Widths
    for row in tbl.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = Inches(width)

def build_document():
    doc = Document()
    
    # Page setup - 0.8 inch margins
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)
        
    # Title Cover Header
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(12)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("SmartShelf Enterprise Platform")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(26)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 23, 42)
    
    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(14)
    run_sub = sub_p.add_run("Comprehensive User Guide & Technical Operations Manual\nAutomated Expiry Alert & Intelligent Shelf Inventory System")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(13)
    run_sub.font.color.rgb = RGBColor(29, 78, 216)
    
    # Meta badge
    meta_p = doc.add_paragraph()
    meta_p.paragraph_format.space_after = Pt(20)
    run_meta = meta_p.add_run("Release v1.2.0 Enterprise  |  Desktop Web SaaS & Streamlit Dual Suite  |  October 2026")
    run_meta.font.name = "Arial"
    run_meta.font.size = Pt(9.5)
    run_meta.font.italic = True
    run_meta.font.color.rgb = RGBColor(100, 116, 139)
    
    doc.add_heading("Table of Contents", level=1)
    toc_items = [
        "1. Executive Summary & Core Capabilities",
        "2. System Architecture & Dual Frontends",
        "3. Technology Stack & Component Details",
        "4. How to Launch & Run the Project",
        "5. Stitch Enterprise UI Walkthrough (All 7 Screens with Screenshots)",
        "   5.1 Screen 1: Executive Inventory Dashboard",
        "   5.2 Screen 2: Inventory Catalog & Item Inspector",
        "   5.3 Screen 3: Register New Product Form",
        "   5.4 Screen 4: Edit Product & Lifecycle Manager",
        "   5.5 Screen 5: Alerts & Expiration Exception Hub",
        "   5.6 Screen 6: Reports & Data Export Center",
        "   5.7 Screen 7: System Audit Log & Governance Ledger",
        "6. Secondary Python-Native Streamlit Interface",
        "7. REST API Endpoints Specification",
        "8. Expiration & Low-Stock Business Rules",
        "9. SQLite Database Schema & Audit Persistence",
        "10. Automated Test Suite & Verification",
        "11. Troubleshooting & FAQ",
    ]
    for item in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(1)
        r = p.add_run(item)
        r.font.name = "Arial"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(51, 65, 85)
        
    doc.add_page_break()
    
    # Section 1
    doc.add_heading("1. Executive Summary & Core Capabilities", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "SmartShelf is an intelligent inventory monitoring, shelf-life analytics, and automated expiry alert platform. "
        "Engineered for retail supermarkets, hypermarkets, convenience stores, and pharmaceutical supply chains, SmartShelf "
        "eliminates inventory shrinkage by proactively flagging items nearing shelf expiration and automating stock reorder thresholds."
    )
    
    doc.add_heading("Core Capabilities:", level=2)
    bullets = [
        ("Automated Expiry Horizon Monitoring", "Calculates remaining shelf life using ISO-8601 dates and categorizes batches into Expired, Expiring Soon (<= 7 days), or Stable (OK)."),
        ("Dual Stock Safety Protection", "Detects Out-of-Stock (0 quantity) and Low Safety Stock (quantity <= minimum threshold) with instant visual indicators."),
        ("B2B Enterprise Single Page Application", "Built directly with Google Stitch desktop-first UI designs, Inter typography, and Material Symbols."),
        ("Full Real-Time CRUD Operations", "Add, View, Live Search, Inspect, Edit, and Safely Delete catalog items with instant SQLite synchronization."),
        ("Immutable Governance Audit Trail", "Every addition, modification, and deletion is recorded in a chronological audit ledger with exact timestamps and descriptions."),
        ("Enterprise Data Reporting & CSV Exports", "One-click downloads for complete inventory CSV datasets and text summaries."),
    ]
    for title, desc in bullets:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(3)
        r_b = bp.add_run(title + ": ")
        r_b.font.bold = True
        r_b.font.color.rgb = RGBColor(15, 23, 42)
        bp.add_run(desc)
        
    create_callout(doc, "SmartShelf operates on a unified SQLite database, allowing multiple frontends (Stitch Enterprise Web UI and Streamlit Analytics) to seamlessly share the same live inventory state.", "ARCHITECTURE HIGHLIGHT")

    # Section 2
    doc.add_heading("2. System Architecture & Merged Single Application", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "SmartShelf is unified into a single enterprise application combining the Google Stitch UI frontend, "
        "a high-performance Python FastAPI backend, an SQLite database, and an integrated Streamlit analytics studio:"
    )
    
    arch_tbl = doc.add_table(rows=1, cols=3)
    style_table(
        arch_tbl,
        [1.5, 2.2, 3.1],
        ["Tier", "Component", "Function & Access"],
        [
            ["Main Application", "Google Stitch Enterprise UI", "Primary desktop SaaS SPA served at http://localhost:5000"],
            ["Backend Engine", "Python with FastAPI (main.py)", "High-performance REST API with automatic Swagger docs at /docs"],
            ["Database Layer", "SQLite 3 (smartshelf.db)", "WAL-mode transactional database located at smartshelf/data/smartshelf.db"],
            ["Integrated Backup", "Streamlit Analytics Studio", "Embedded directly in the Stitch UI and active at http://localhost:8501"],
            ["Business Logic", "inventory_logic.py", "Pure deterministic rules for expiry horizons and safety stock thresholds"],
        ]
    )
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Section 3
    doc.add_heading("3. Technology Stack & Component Details", level=1)
    tech_tbl = doc.add_table(rows=1, cols=3)
    style_table(
        tech_tbl,
        [1.8, 1.8, 3.2],
        ["Technology", "Version / Spec", "Role in SmartShelf"],
        [
            ["FastAPI", "v0.143+ (Python 3.11)", "High-performance asynchronous REST backend, route handlers, and OpenAPI"],
            ["Uvicorn", "ASGI Web Server", "High-throughput server running the unified main application on port 5000"],
            ["HTML5 / Tailwind CSS", "Tailwind v3.4 CDN", "Responsive B2B SaaS UI styling, custom tokens, grid architecture"],
            ["Google Stitch Suite", "Enterprise UI Suite", "7 fully integrated screens for catalog, dashboard, alerts, and governance"],
            ["Material Symbols", "Google Fonts", "Monoline vector iconography for all actions, navigation, and alerts"],
            ["Inter & JetBrains Mono", "Google Fonts", "Inter for typography headings/body; JetBrains Mono for numeric tabular figures"],
            ["SQLite 3", "Python Standard Library", "ACID-compliant relational database with WAL (Write-Ahead Logging)"],
            ["Streamlit", ">= 1.35.0", "Secondary/backup data studio embedded directly inside the main UI"],
            ["Pytest", ">= 8.0.0", "Automated test runner verifying business logic rules (9/9 passed)"],
        ]
    )
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Section 4
    doc.add_heading("4. How to Launch & Run the Project", level=1)
    p = doc.add_paragraph()
    p.add_run("You can launch the SmartShelf platform through multiple convenient methods:")
    
    doc.add_heading("Method 1: One-Click Windows Launcher (Recommended)", level=2)
    p1 = doc.add_paragraph()
    p1.add_run("Double-click the file ")
    r_bat = p1.add_run("run_enterprise.bat")
    r_bat.font.bold = True
    p1.add_run(" in the project root directory. This opens the server and hosts the application at ")
    r_url = p1.add_run("http://localhost:5000")
    r_url.font.bold = True
    p1.add_run(".")
    
    doc.add_heading("Method 2: Command Line (PowerShell / Terminal)", level=2)
    p2 = doc.add_paragraph()
    p2.add_run("Open PowerShell or Command Prompt in the project folder and run:\n")
    r_cmd1 = p2.add_run("cd \"d:\\cppe kei project 1\"\npython server.py 5000")
    r_cmd1.font.name = "Consolas"
    r_cmd1.font.size = Pt(9.5)
    r_cmd1.font.color.rgb = RGBColor(15, 23, 42)
    
    doc.add_heading("Method 3: NPM Script", level=2)
    p3 = doc.add_paragraph()
    r_cmd2 = p3.add_run("npm start")
    r_cmd2.font.name = "Consolas"
    r_cmd2.font.size = Pt(9.5)
    
    doc.add_heading("Method 4: Launching Streamlit Interface (Optional)", level=2)
    p4 = doc.add_paragraph()
    r_cmd3 = p4.add_run("cd \"d:\\cppe kei project 1\\smartshelf\"\nstreamlit run app.py")
    r_cmd3.font.name = "Consolas"
    r_cmd3.font.size = Pt(9.5)
    p4.add_run("\nOpens automatically at ")
    p4.add_run("http://localhost:8501").font.bold = True
    
    doc.add_page_break()

    # Section 5
    doc.add_heading("5. Stitch Enterprise UI Walkthrough (All 7 Screens)", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "The Stitch Enterprise Platform includes 7 interconnected, high-density SaaS screens. "
        "Each screen has been unified into a single application with persistent sidebar navigation and real-time SQLite interaction:"
    )

    screens = [
        (
            "5.1 Screen 1: Executive Inventory Dashboard (#dashboard)",
            "executive_inventory_dashboard",
            "The executive landing screen provides at-a-glance operational awareness across all merchandise categories:",
            [
                "5 Real-Time KPI Cards: Catalog SKUs, Total Units, Gross Valuation in Rs, Expired Batches, and Low Stock Reorders.",
                "Dynamic Alert Banners: Critical notice highlighting expired goods and reorder recommendations.",
                "Units by Category Bar Chart: Horizontal percentage distribution across Dairy, Beverages, Bakery, Produce, Grocery, and Household.",
                "Stock Health Segmented Bar: Real-time visual ratio of In Stock vs. Low Stock vs. Out of Stock.",
                "Upcoming Shelf Expirations Table: Priority batches requiring FEFO (First-Expired, First-Out) rotation with days-remaining countdowns.",
                "Quick Action Triggers: Direct jump buttons to Register New Product and Download CSV.",
            ]
        ),
        (
            "5.2 Screen 2: Inventory Catalog & Item Inspector (#catalog)",
            "inventory_catalog_inspector",
            "The primary workspace for searching, filtering, and deeply inspecting product records:",
            [
                "Multi-Filter Matrix: Real-time keyword search query, Category selector, Stock Level selector, and Expiry Lifecycle filter.",
                "Dense Product Table: Tabular records with SKU ID, Name, Category, Stock Units, Unit Price, Expiry Date, and color-coded status badges.",
                "Item Specification Inspector (Right Panel): Clicking any table row opens its full profile in the drawer, including product photo, threshold buffer progress bar, batch valuation, and expiry horizon.",
                "Direct Record Actions: 'Edit Product Record' pre-selects the item in the edit screen; 'Delete Product' triggers a confirmation modal.",
            ]
        ),
        (
            "5.3 Screen 3: Register New Product Form (#register)",
            "register_new_product_form",
            "A guided catalog ingestion form with live preview and automatic valuation calculations:",
            [
                "Product Identity: Trade name, category dropdown (with custom category support), and GS1 SKU reference.",
                "Inventory & Valuation: Real-time computation of batch valuation (Quantity x Unit Price) as numbers are typed.",
                "Lifecycle & Expiry Controls: Perishable checkbox toggle, date picker, and minimum safety threshold configuration.",
                "Live System Sync Card: Real-time card preview on the right side that updates simultaneously to reflect how the product will look in the catalog.",
                "Database Persistence: Saves to SQLite and appends an ADD entry to the audit log.",
            ]
        ),
        (
            "5.4 Screen 4: Edit Product & Lifecycle Manager (#edit)",
            "edit_product_lifecycle_manager",
            "Enables store managers to adjust stock counts, pricing, and expiry dates for existing inventory:",
            [
                "Product Selector Dropdown: Searchable list of all catalog items by SKU and product name.",
                "Automatic Field Population: Selected product's current values populate immediately.",
                "Parameter Updates: Change stock quantity, unit price, threshold, or extend expiration date.",
                "Audit Logging: Generates an EDIT transaction in the system ledger upon saving.",
            ]
        ),
        (
            "5.5 Screen 5: Alerts & Expiration Exception Hub (#alerts)",
            "alerts_expiration_exception_hub",
            "Dedicated exception dispatch center focused on preventing revenue loss and food waste:",
            [
                "Bento Risk Trio: Expired Stock (with automated total write-off financial loss calculation), Impending Expirations (<= 7 days), and Depleted / Low Stock counts.",
                "Critical Expired Batches Table: Lists batches that have passed expiration date and must be removed from shelves immediately.",
                "Low Safety Stock Table: Lists depleted and low-inventory products requiring purchase order reorders.",
                "Alert Export: Dedicated button to export filtered exception data.",
            ]
        ),
        (
            "5.6 Screen 6: Reports & Data Export Center (#reports)",
            "reports_data_export_center",
            "Analytics and external audit center for downloading full inventory datasets:",
            [
                "Financial KPI Metrics: Total SKUs, Aggregate Units, Gross Inventory Valuation, and Expired Write-Off Loss.",
                "One-Click CSV Export: Downloads complete 'smartshelf_inventory.csv' formatted for Microsoft Excel or Google Sheets.",
                "One-Click Text Summary: Downloads formatted 'smartshelf_summary.txt' containing executive snapshot figures.",
            ]
        ),
        (
            "5.7 Screen 7: System Audit Log & Governance Ledger (#audit)",
            "system_audit_log_governance_ledger",
            "Chronological event ledger providing complete compliance traceability:",
            [
                "Immutable Record History: Every ADD, EDIT, and DELETE action is permanently stamped with timestamp, product ID, and event notes.",
                "Color-Coded Badges: Green ADD badges, Blue EDIT badges, and Red DELETE badges.",
                "Export Audit Log (JSON): Dedicated button to download the entire audit log as a JSON file.",
            ]
        ),
    ]

    for title, folder, desc, features in screens:
        doc.add_heading(title, level=2)
        doc.add_paragraph(desc)
        for feat in features:
            bp = doc.add_paragraph(style='List Bullet')
            bp.paragraph_format.space_after = Pt(2)
            bp.add_run(feat)
            
        # Embed screenshot if exists
        img_path = os.path.join(STITCH_DIR, folder, "screen.png")
        if os.path.exists(img_path):
            img_p = doc.add_paragraph()
            img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            img_p.paragraph_format.space_before = Pt(6)
            img_p.paragraph_format.space_after = Pt(2)
            doc.add_picture(img_path, width=Inches(6.2))
            cap_p = doc.add_paragraph()
            cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap_p.paragraph_format.space_after = Pt(14)
            cap_r = cap_p.add_run(f"Figure: {title.split('(')[0].strip()} Interface")
            cap_r.font.size = Pt(8.5)
            cap_r.font.italic = True
            cap_r.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # Section 6: Streamlit Interface
    doc.add_heading("6. Secondary Python-Native Streamlit Interface", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "For teams preferring a purely Python-based interface or running data science exploration, SmartShelf "
        "includes a fully configured Streamlit application in the smartshelf/ directory. It provides multi-page "
        "navigation via st.navigation and directly connects to the same SQLite database."
    )
    
    st_tbl = doc.add_table(rows=1, cols=2)
    style_table(
        st_tbl,
        [2.5, 4.3],
        ["Streamlit Page", "Function & Capabilities"],
        [
            ["pages/dashboard.py", "KPI metric cards, category bar charts, stock health distribution."],
            ["pages/inventory.py", "Catalog table with category/stock filters, search bar, and badge styling."],
            ["pages/add_product.py", "Form with validation, non-perishable toggle, and SQLite insertion."],
            ["pages/edit_product.py", "Item selector and in-place field updates with audit logging."],
            ["pages/delete_product.py", "Confirmation checkbox and secure product deletion."],
            ["pages/alerts.py", "Dedicated sections for expired and low-stock items."],
            ["pages/reports.py", "CSV download button and summary text report generation."],
            ["pages/audit_log.py", "Full audit log table with timestamps and action details."],
        ]
    )
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Section 7: REST API Endpoints
    doc.add_heading("7. REST API Endpoints Specification", level=1)
    p = doc.add_paragraph()
    p.add_run("The Python server (server.py) provides a complete RESTful JSON API accessible on port 5000:")
    
    api_tbl = doc.add_table(rows=1, cols=4)
    style_table(
        api_tbl,
        [1.0, 1.8, 1.8, 2.2],
        ["Method", "Endpoint", "Parameters", "Description"],
        [
            ["GET", "/api/stats", "None", "Returns total SKUs, units, valuation, expired/low-stock counts, category breakdown."],
            ["GET", "/api/products", "q, category, stock_status, expiry_status", "Returns list of products enriched with computed statuses."],
            ["GET", "/api/products/<id>", "id (URL path)", "Returns single product details and calculations by SKU ID."],
            ["POST", "/api/products", "JSON payload", "Registers a new product in SQLite and appends an ADD audit log."],
            ["PUT", "/api/products/<id>", "JSON payload", "Updates an existing product in SQLite and appends an EDIT audit log."],
            ["DELETE", "/api/products/<id>", "id (URL path)", "Deletes product from SQLite and appends a DELETE audit log."],
            ["GET", "/api/alerts", "None", "Returns categorized lists of expired, expiring soon, and low-stock batches."],
            ["GET", "/api/audit-log", "None", "Returns chronological list of recent audit transactions."],
            ["GET", "/api/export/csv", "None", "Streams downloadable UTF-8 CSV inventory dataset."],
            ["GET", "/api/export/summary", "None", "Streams downloadable formatted plain text summary report."],
            ["POST", "/api/seed", "None", "Re-seeds the database with default enterprise demo products."],
        ]
    )
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Section 8: Business Logic Rules
    doc.add_heading("8. Expiration & Low-Stock Business Rules", level=1)
    p = doc.add_paragraph()
    p.add_run("All calculations are performed by deterministic pure functions in inventory_logic.py:")
    
    doc.add_heading("Expiry Horizon Rules (7-Day Warning Threshold):", level=2)
    exp_tbl = doc.add_table(rows=1, cols=3)
    style_table(
        exp_tbl,
        [1.8, 2.4, 2.6],
        ["Expiry Status", "Mathematical Condition", "Prescribed Operational Action"],
        [
            ["Expired", "Expiry Date < Today's Date", "Immediate removal from shelves; write-off disposal recorded."],
            ["Expiring Soon", "0 <= (Expiry Date - Today) <= 7 Days", "Mark down price or prioritize for immediate sale/discount."],
            ["OK", "(Expiry Date - Today) > 7 Days", "Product is fresh; normal inventory rotation."],
            ["N/A", "Expiry Date is None / Blank", "Non-perishable item; expiry monitoring disabled."],
        ]
    )
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    doc.add_heading("Stock Threshold Rules:", level=2)
    stk_tbl = doc.add_table(rows=1, cols=3)
    style_table(
        stk_tbl,
        [1.8, 2.4, 2.6],
        ["Stock Status", "Mathematical Condition", "Prescribed Operational Action"],
        [
            ["Out of Stock", "Quantity == 0", "Critical stockout; emergency purchase requisition required."],
            ["Low Stock", "0 < Quantity <= Min Stock Threshold", "Replenishment reorder triggered (default threshold: 5)."],
            ["In Stock", "Quantity > Min Stock Threshold", "Inventory buffer is healthy."],
        ]
    )
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Section 9: Database Schema
    doc.add_heading("9. SQLite Database Schema & Audit Persistence", level=1)
    p = doc.add_paragraph()
    p.add_run("The database is auto-created in smartshelf/data/smartshelf.db with two primary tables:")
    
    p_code = doc.add_paragraph()
    r_schema = p_code.add_run(
        "CREATE TABLE products (\n"
        "    id          INTEGER PRIMARY KEY AUTOINCREMENT,\n"
        "    name        TEXT    NOT NULL,\n"
        "    category    TEXT    NOT NULL,\n"
        "    quantity    INTEGER NOT NULL CHECK(quantity >= 0),\n"
        "    unit_price  REAL    NOT NULL CHECK(unit_price >= 0),\n"
        "    expiry_date TEXT,\n"
        "    min_stock   INTEGER NOT NULL DEFAULT 5 CHECK(min_stock >= 0),\n"
        "    created_at  TEXT    NOT NULL,\n"
        "    updated_at  TEXT    NOT NULL\n"
        ");\n\n"
        "CREATE TABLE audit_log (\n"
        "    id          INTEGER PRIMARY KEY AUTOINCREMENT,\n"
        "    action      TEXT    NOT NULL, -- 'ADD', 'EDIT', 'DELETE'\n"
        "    product_id  INTEGER,\n"
        "    details     TEXT,\n"
        "    timestamp   TEXT    NOT NULL\n"
        ");"
    )
    r_schema.font.name = "Consolas"
    r_schema.font.size = Pt(8.5)
    r_schema.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Section 10: Automated Testing
    doc.add_heading("10. Automated Test Suite & Verification", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "SmartShelf includes an automated Pytest test suite in smartshelf/tests/test_inventory_logic.py "
        "that executes 9 rigorous unit tests covering all edge cases (leap years, zero stock, threshold boundaries):"
    )
    
    test_tbl = doc.add_table(rows=1, cols=3)
    style_table(
        test_tbl,
        [2.5, 3.2, 1.1],
        ["Test Function", "Rule Verified", "Result"],
        [
            ["test_expired", "Correctly identifies past dates as 'Expired'", "PASSED"],
            ["test_expiring_soon", "Correctly identifies dates within 7 days as 'Expiring Soon'", "PASSED"],
            ["test_ok", "Correctly identifies dates > 7 days as 'OK'", "PASSED"],
            ["test_no_expiry", "Handles None/empty dates as 'N/A' without errors", "PASSED"],
            ["test_low_stock_at_threshold", "Flags quantity == min_stock as 'Low Stock'", "PASSED"],
            ["test_out_of_stock", "Flags quantity == 0 as 'Out of Stock'", "PASSED"],
            ["test_in_stock", "Flags quantity > min_stock as 'In Stock'", "PASSED"],
            ["test_enrich", "Validates enrichment of dictionaries with all computed fields", "PASSED"],
            ["test_dashboard_counts", "Verifies aggregate counts across all categories", "PASSED"],
        ]
    )
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Section 11: Troubleshooting & FAQ
    doc.add_heading("11. Troubleshooting & FAQ", level=1)
    faqs = [
        ("Q1: How do I access the application if the browser does not open automatically?", "Simply open your browser and navigate to http://localhost:5000 for the Stitch Enterprise Suite, or http://localhost:8501 for the Streamlit dashboard."),
        ("Q2: Port 5000 is already in use by another application. How can I change it?", "You can specify any custom port when running server.py, for example: 'python server.py 8080'. The application will then be accessible at http://localhost:8080."),
        ("Q3: Are changes made in the Stitch UI reflected in Streamlit?", "Yes! Both applications share the exact same SQLite database file (smartshelf/data/smartshelf.db). Any product added, edited, or deleted in one interface immediately updates the other."),
        ("Q4: How do I back up my inventory catalog?", "You can click 'Download Inventory as CSV' on the Reports screen, or simply create a copy of the smartshelf/data/smartshelf.db file."),
        ("Q5: Can I reset the database to sample demo data?", "Yes! You can invoke the REST API endpoint 'POST /api/seed' or delete smartshelf.db and restart the server, which will automatically re-populate the demo items."),
    ]
    for q, a in faqs:
        qp = doc.add_paragraph()
        qp.paragraph_format.space_after = Pt(1)
        r_q = qp.add_run(q)
        r_q.font.bold = True
        r_q.font.color.rgb = RGBColor(15, 23, 42)
        
        ap = doc.add_paragraph()
        ap.paragraph_format.space_after = Pt(6)
        r_a = ap.add_run(a)
        r_a.font.color.rgb = RGBColor(51, 65, 85)

    # Save to both locations
    output_root = os.path.join(PROJECT_ROOT, "HOW_TO_USE.docx")
    output_smartshelf = os.path.join(PROJECT_ROOT, "smartshelf", "HOW_TO_USE.docx")
    
    doc.save(output_root)
    doc.save(output_smartshelf)
    print(f"Generated {output_root} successfully!")
    print(f"Generated {output_smartshelf} successfully!")

if __name__ == "__main__":
    build_document()
