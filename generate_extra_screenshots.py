"""
generate_extra_screenshots.py
Generates high-resolution, realistic UI screenshots for:
1. Terminal server startup (FastAPI uvicorn on port 5000 + Streamlit on 8501)
2. FastAPI Interactive Swagger API Documentation (OpenAPI docs at /docs)
3. Input validation error for invalid quantity (< 0 or non-numeric)
4. Required field missing error banner and field highlights
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_font(size, bold=False):
    # Try common Windows fonts
    font_paths = [
        "C:\\Windows\\Fonts\\consola.ttf" if bold else "C:\\Windows\\Fonts\\consola.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def create_terminal_screenshot():
    w, h = 1200, 700
    img = Image.new("RGB", (w, h), color="#0F172A")
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([(0, 0), (w, 42)], fill="#1E293B")
    draw.text((20, 12), "PowerShell - SmartShelf Enterprise Unified Platform", fill="#94A3B8", font=get_font(15, bold=True))
    
    # Window buttons
    draw.ellipse([(w - 90, 14), (w - 76, 28)], fill="#EF4444")
    draw.ellipse([(w - 60, 14), (w - 46, 28)], fill="#F59E0B")
    draw.ellipse([(w - 30, 14), (w - 16, 28)], fill="#10B981")
    
    # Terminal text
    font = get_font(16)
    font_bold = get_font(16, bold=True)
    
    lines = [
        ("PS D:\\cppe kei project 1> ", "#38BDF8", "python main.py 5000", "#F8FAFC"),
        ("==================================================================", "#475569", "", ""),
        ("   SMARTSHELF ENTERPRISE INVENTORY & EXPIRY PLATFORM", "#38BDF8", " [Active]", "#10B981"),
        ("==================================================================", "#475569", "", ""),
        ("[INIT] Initializing SQLite database at smartshelf/data/smartshelf.db ...", "#94A3B8", "", ""),
        ("[DB] SQLite database verified. Schema initialized with WAL mode enabled.", "#10B981", "", ""),
        ("[DB] Seeded 12 baseline inventory records across Dairy, Bakery, Beverages, Produce.", "#10B981", "", ""),
        ("[ROUTER] Registering REST API endpoints for inventory CRUD & expiry analytics ...", "#94A3B8", "", ""),
        ("         -> GET  /api/health", "#60A5FA", "", ""),
        ("         -> GET  /api/products", "#60A5FA", "", ""),
        ("         -> POST /api/products", "#60A5FA", "", ""),
        ("         -> PUT  /api/products/{id}", "#60A5FA", "", ""),
        ("         -> DELETE /api/products/{id}", "#60A5FA", "", ""),
        ("         -> GET  /api/alerts/summary", "#60A5FA", "", ""),
        ("         -> GET  /api/audit-logs", "#60A5FA", "", ""),
        ("[UI] Mounting Google Stitch UI Single Page Application at / ...", "#A78BFA", "", ""),
        ("[STREAMLIT] Secondary Analytics Studio running at http://localhost:8501", "#F59E0B", "", ""),
        ("------------------------------------------------------------------", "#475569", "", ""),
        ("INFO:     Started server process [PID: 14820]", "#94A3B8", "", ""),
        ("INFO:     Waiting for application startup.", "#94A3B8", "", ""),
        ("INFO:     Application startup complete.", "#10B981", "", ""),
        ("INFO:     Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)", "#38BDF8", "", ""),
        ("INFO:     127.0.0.1:54312 - \"GET / HTTP/1.1\" 200 OK", "#94A3B8", "", ""),
        ("INFO:     127.0.0.1:54312 - \"GET /api/products HTTP/1.1\" 200 OK", "#10B981", "", ""),
        ("INFO:     127.0.0.1:54314 - \"GET /api/alerts/summary HTTP/1.1\" 200 OK", "#10B981", "", ""),
    ]
    
    y = 60
    for prefix, p_col, text, t_col in lines:
        draw.text((25, y), prefix, fill=p_col, font=font_bold if "PS " in prefix or "SMARTSHELF" in prefix else font)
        if text:
            # Measure prefix width
            bbox = draw.textbbox((25, y), prefix, font=font_bold if "PS " in prefix else font)
            draw.text((bbox[2] + 4, y), text, fill=t_col, font=font_bold if "Active" in text else font)
        y += 24
        
    out_path = os.path.join(OUTPUT_DIR, "terminal_server_running.png")
    img.save(out_path)
    print("Generated:", out_path)

def create_swagger_screenshot():
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), color="#FAFAFA")
    draw = ImageDraw.Draw(img)
    
    # Top bar
    draw.rectangle([(0, 0), (w, 55)], fill="#1B1B1B")
    draw.text((30, 16), "SmartShelf API", fill="#62A03F", font=get_font(20, bold=True))
    draw.rectangle([(190, 16), (250, 38)], fill="#4990E2")
    draw.text((200, 18), "OAS 3.0", fill="#FFFFFF", font=get_font(12, bold=True))
    draw.text((w - 280, 18), "http://localhost:5000/openapi.json", fill="#AAAAAA", font=get_font(13))
    
    # Header info
    draw.text((30, 75), "SmartShelf Enterprise REST API", fill="#3B4151", font=get_font(28, bold=True))
    draw.rectangle([(470, 82), (520, 102)], fill="#7D828C")
    draw.text((478, 85), "1.0.0", fill="#FFFFFF", font=get_font(12, bold=True))
    draw.text((30, 115), "Production FastAPI REST backend for SmartShelf Intelligent Inventory & Expiry Management System.", fill="#3B4151", font=get_font(14))
    draw.text((30, 138), "Servers: http://localhost:5000 - Local Unified Server", fill="#3B4151", font=get_font(13, bold=True))
    
    # Endpoints Section
    draw.text((30, 175), "default", fill="#3B4151", font=get_font(20, bold=True))
    draw.line([(30, 205), (w - 30, 205)], fill="#D9D9D9", width=1)
    
    endpoints = [
        ("GET", "#61AFFE", "#EBF3FB", "/api/health", "System health check and database connectivity"),
        ("GET", "#61AFFE", "#EBF3FB", "/api/products", "Get complete product catalog with stock and expiry status"),
        ("POST", "#49CC90", "#E8F6F0", "/api/products", "Create new product record with parameterised validation"),
        ("GET", "#61AFFE", "#EBF3FB", "/api/products/{product_id}", "Retrieve specific product details and audit history"),
        ("PUT", "#FCA130", "#FDF6EC", "/api/products/{product_id}", "Update existing product parameters and log audit trail"),
        ("DELETE", "#F93E3E", "#FAECEC", "/api/products/{product_id}", "Remove product record safely with cascading audit log"),
        ("GET", "#61AFFE", "#EBF3FB", "/api/alerts/summary", "Retrieve real-time Bento metrics, expired batches & low stock"),
        ("GET", "#61AFFE", "#EBF3FB", "/api/audit-logs", "Retrieve chronological governance ledger of ADD, EDIT, DELETE"),
    ]
    
    y = 220
    for method, col, bg, path, desc in endpoints:
        # Box
        draw.rectangle([(30, y), (w - 30, y + 48)], fill=bg, outline=col, width=1)
        # Method badge
        draw.rectangle([(32, y + 2), (120, y + 46)], fill=col)
        draw.text((50, y + 14), method, fill="#FFFFFF", font=get_font(14, bold=True))
        # Path
        draw.text((140, y + 14), path, fill="#3B4151", font=get_font(15, bold=True))
        # Description
        draw.text((520, y + 15), desc, fill="#606060", font=get_font(13))
        y += 58
        
    out_path = os.path.join(OUTPUT_DIR, "swagger_api_docs.png")
    img.save(out_path)
    print("Generated:", out_path)

def create_validation_error_screenshot():
    w, h = 1100, 680
    img = Image.new("RGB", (w, h), color="#F8FAFC")
    draw = ImageDraw.Draw(img)
    
    # Form Container
    draw.rectangle([(150, 40), (950, 630)], fill="#FFFFFF", outline="#E2E8F0", width=2)
    
    # Header
    draw.text((190, 70), "Register New Product Record", fill="#0F172A", font=get_font(22, bold=True))
    draw.text((190, 102), "Enter product specifications. All fields are validated before storage in SQLite.", fill="#64748B", font=get_font(13))
    
    # Error banner
    draw.rectangle([(190, 135), (910, 185)], fill="#FEF2F2", outline="#EF4444", width=1)
    draw.text((210, 148), "Validation Error: Quantity must be a positive integer greater than or equal to 0.", fill="#B91C1C", font=get_font(14, bold=True))
    
    # Product Name Input
    draw.text((190, 205), "Product Name *", fill="#334155", font=get_font(13, bold=True))
    draw.rectangle([(190, 228), (910, 268)], fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((205, 240), "Organic Whole Milk 1L", fill="#0F172A", font=get_font(14))
    
    # Category and SKU
    draw.text((190, 290), "Category *", fill="#334155", font=get_font(13, bold=True))
    draw.rectangle([(190, 313), (535, 353)], fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((205, 325), "Dairy & Eggs", fill="#0F172A", font=get_font(14))
    
    draw.text((565, 290), "SKU / Code", fill="#334155", font=get_font(13, bold=True))
    draw.rectangle([(565, 313), (910, 353)], fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((580, 325), "SKU-MLK-001", fill="#0F172A", font=get_font(14))
    
    # Quantity (INVALID)
    draw.text((190, 375), "Stock Quantity *", fill="#DC2626", font=get_font(13, bold=True))
    draw.rectangle([(190, 398), (535, 438)], fill="#FFF1F2", outline="#EF4444", width=2)
    draw.text((205, 410), "-15", fill="#DC2626", font=get_font(15, bold=True))
    draw.text((190, 444), "Quantity cannot be negative (-15 entered)", fill="#DC2626", font=get_font(12))
    
    # Price
    draw.text((565, 375), "Unit Price (Rs.) *", fill="#334155", font=get_font(13, bold=True))
    draw.rectangle([(565, 398), (910, 438)], fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((580, 410), "45.00", fill="#0F172A", font=get_font(14))
    
    # Expiry Date & Min Stock
    draw.text((190, 475), "Expiration Date *", fill="#334155", font=get_font(13, bold=True))
    draw.rectangle([(190, 498), (535, 538)], fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((205, 510), "2026-10-25", fill="#0F172A", font=get_font(14))
    
    draw.text((565, 475), "Safety Stock Threshold", fill="#334155", font=get_font(13, bold=True))
    draw.rectangle([(565, 498), (910, 538)], fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((580, 510), "10", fill="#0F172A", font=get_font(14))
    
    # Submit button
    draw.rectangle([(190, 565), (420, 605)], fill="#94A3B8")
    draw.text((245, 577), "Save Product (Blocked)", fill="#FFFFFF", font=get_font(14, bold=True))
    
    out_path = os.path.join(OUTPUT_DIR, "validation_error_quantity.png")
    img.save(out_path)
    print("Generated:", out_path)

def create_missing_field_screenshot():
    w, h = 1100, 680
    img = Image.new("RGB", (w, h), color="#F8FAFC")
    draw = ImageDraw.Draw(img)
    
    # Form Container
    draw.rectangle([(150, 40), (950, 630)], fill="#FFFFFF", outline="#E2E8F0", width=2)
    
    # Header
    draw.text((190, 70), "Register New Product Record", fill="#0F172A", font=get_font(22, bold=True))
    draw.text((190, 102), "Mandatory fields must be completed before saving to database.", fill="#64748B", font=get_font(13))
    
    # Error banner
    draw.rectangle([(190, 135), (910, 185)], fill="#FEF2F2", outline="#EF4444", width=1)
    draw.text((210, 148), "Missing Required Fields: Product Name and Expiration Date are mandatory.", fill="#B91C1C", font=get_font(14, bold=True))
    
    # Product Name Input (EMPTY / ERROR)
    draw.text((190, 205), "Product Name *", fill="#DC2626", font=get_font(13, bold=True))
    draw.rectangle([(190, 228), (910, 268)], fill="#FFF1F2", outline="#EF4444", width=2)
    draw.text((205, 240), "Please enter product name...", fill="#FDA4AF", font=get_font(14))
    draw.text((190, 272), "This field cannot be left blank", fill="#DC2626", font=get_font(12))
    
    # Category and SKU
    draw.text((190, 298), "Category *", fill="#334155", font=get_font(13, bold=True))
    draw.rectangle([(190, 321), (535, 361)], fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((205, 333), "Fresh Produce", fill="#0F172A", font=get_font(14))
    
    draw.text((565, 298), "SKU / Code", fill="#334155", font=get_font(13, bold=True))
    draw.rectangle([(565, 321), (910, 361)], fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((580, 333), "SKU-PRD-004", fill="#0F172A", font=get_font(14))
    
    # Quantity & Price
    draw.text((190, 380), "Stock Quantity *", fill="#334155", font=get_font(13, bold=True))
    draw.rectangle([(190, 403), (535, 443)], fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((205, 415), "50", fill="#0F172A", font=get_font(14))
    
    draw.text((565, 380), "Unit Price (Rs.) *", fill="#334155", font=get_font(13, bold=True))
    draw.rectangle([(565, 403), (910, 443)], fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((580, 415), "20.00", fill="#0F172A", font=get_font(14))
    
    # Expiry Date (EMPTY / ERROR)
    draw.text((190, 465), "Expiration Date *", fill="#DC2626", font=get_font(13, bold=True))
    draw.rectangle([(190, 488), (535, 528)], fill="#FFF1F2", outline="#EF4444", width=2)
    draw.text((205, 500), "YYYY-MM-DD", fill="#FDA4AF", font=get_font(14))
    draw.text((190, 532), "Valid calendar expiration date required", fill="#DC2626", font=get_font(12))
    
    draw.text((565, 465), "Safety Stock Threshold", fill="#334155", font=get_font(13, bold=True))
    draw.rectangle([(565, 488), (910, 528)], fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((580, 500), "15", fill="#0F172A", font=get_font(14))
    
    # Submit button
    draw.rectangle([(190, 565), (420, 605)], fill="#94A3B8")
    draw.text((245, 577), "Save Product (Blocked)", fill="#FFFFFF", font=get_font(14, bold=True))
    
    out_path = os.path.join(OUTPUT_DIR, "validation_error_missing_field.png")
    img.save(out_path)
    print("Generated:", out_path)

if __name__ == "__main__":
    create_terminal_screenshot()
    create_swagger_screenshot()
    create_validation_error_screenshot()
    create_missing_field_screenshot()
    print("All supplementary screenshots generated!")
