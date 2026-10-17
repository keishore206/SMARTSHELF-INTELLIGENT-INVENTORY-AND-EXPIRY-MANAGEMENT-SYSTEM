"""
create_diagrams.py
Generates high-resolution academic diagrams for the SmartShelf project report:
1. Figure 3.1: System Architecture Diagram
2. Figure 4.1: Activity Diagram for Data Engineering
3. Figure 4.2: Activity Diagram for Cloud Engineering
4. Figure 4.3: Activity Diagram for AI Engineering (Rule-Based Logic)
5. Figure 4.4: Activity Diagram for Security Engineering
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def draw_rounded_box(ax, xy, width, height, text, title=None, facecolor="#EFF4FF", edgecolor="#1D4ED8", textcolor="#0F172A", fontsize=10, boxstyle="round,pad=0.4,rounding_size=0.15"):
    box = patches.FancyBboxPatch(
        xy, width, height,
        boxstyle=boxstyle,
        linewidth=1.8,
        edgecolor=edgecolor,
        facecolor=facecolor,
        zorder=2
    )
    ax.add_patch(box)
    cx = xy[0] + width / 2.0
    cy = xy[1] + height / 2.0
    
    if title:
        ax.text(cx, cy + height * 0.2, title, ha="center", va="center", fontsize=fontsize + 1, fontweight="bold", color=edgecolor, zorder=3)
        ax.text(cx, cy - height * 0.15, text, ha="center", va="center", fontsize=fontsize - 1, color=textcolor, zorder=3)
    else:
        ax.text(cx, cy, text, ha="center", va="center", fontsize=fontsize, fontweight="semibold", color=textcolor, zorder=3)

def draw_arrow(ax, start, end, label=None, color="#475569", lw=1.8, label_offset=(0, 0)):
    ax.annotate(
        "",
        xy=end, xycoords='data',
        xytext=start, textcoords='data',
        arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=color, lw=lw, shrinkA=3, shrinkB=3),
        zorder=4
    )
    if label:
        mx = (start[0] + end[0]) / 2.0 + label_offset[0]
        my = (start[1] + end[1]) / 2.0 + label_offset[1]
        ax.text(mx, my, label, ha="center", va="center", fontsize=8.5, fontweight="bold", color="#1E293B",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#CBD5E1", lw=0.8), zorder=5)


# ================= 1. FIGURE 3.1: ARCHITECTURE DIAGRAM =================
def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    # Title
    ax.text(5.0, 6.6, "SmartShelf — Three-Tier System Architecture", ha="center", va="center", fontsize=14, fontweight="bold", color="#0F172A")

    # Layer 1: Presentation Layer
    draw_rounded_box(ax, (0.5, 4.4), 9.0, 1.8, "", title="1. PRESENTATION LAYER (CLIENT INTERFACES)", facecolor="#F8FAFC", edgecolor="#64748B", fontsize=11)
    draw_rounded_box(ax, (1.0, 4.6), 3.6, 1.2, "Desktop SaaS B2B SPA\nInter Font, Tailwind, 7 Screens\nhttp://localhost:5000", title="Primary: Google Stitch UI", facecolor="#EFF6FF", edgecolor="#1D4ED8", fontsize=9.5)
    draw_rounded_box(ax, (5.4, 4.6), 3.6, 1.2, "Python-Native Analytics\nMulti-Page App (st.navigation)\nhttp://localhost:8501", title="Backup: Streamlit Studio", facecolor="#F0FDF4", edgecolor="#16A34A", fontsize=9.5)

    # Layer 2: Application / Logic Layer
    draw_rounded_box(ax, (0.5, 2.2), 9.0, 1.8, "", title="2. APPLICATION & LOGIC LAYER (BACKEND & APIs)", facecolor="#F8FAFC", edgecolor="#64748B", fontsize=11)
    draw_rounded_box(ax, (1.0, 2.4), 2.5, 1.2, "REST Endpoints\nOpenAPI Docs (/docs)\nCORS & Async Routing", title="FastAPI Server", facecolor="#EFF6FF", edgecolor="#1D4ED8", fontsize=9.5)
    draw_rounded_box(ax, (3.8, 2.4), 2.5, 1.2, "7-Day Expiry Horizon\nLow Stock Thresholds\nStatus Enrichment", title="inventory_logic.py", facecolor="#FEF3C7", edgecolor="#D97706", fontsize=9.5)
    draw_rounded_box(ax, (6.6, 2.4), 2.5, 1.2, "CSV Dataset Export\nExecutive Text Summary\nTabular Structuring", title="reports.py / Pandas", facecolor="#F3E8FF", edgecolor="#9333EA", fontsize=9.5)

    # Layer 3: Persistence Layer
    draw_rounded_box(ax, (0.5, 0.2), 9.0, 1.6, "", title="3. PERSISTENCE & DATA LAYER (SQLITE DATABASE)", facecolor="#F8FAFC", edgecolor="#64748B", fontsize=11)
    draw_rounded_box(ax, (1.5, 0.4), 3.2, 1.0, "id, name, category, quantity,\nunit_price, expiry_date, min_stock", title="products Table", facecolor="#EFF6FF", edgecolor="#1D4ED8", fontsize=9.5)
    draw_rounded_box(ax, (5.3, 0.4), 3.2, 1.0, "id, action (ADD/EDIT/DELETE),\nproduct_id, details, timestamp", title="audit_log Table", facecolor="#FEF2F2", edgecolor="#DC2626", fontsize=9.5)

    # Connecting Arrows
    draw_arrow(ax, (2.8, 4.6), (2.3, 3.6), label="REST API (HTTP)", label_offset=(0.1, 0))
    draw_arrow(ax, (7.2, 4.6), (5.1, 3.6), label="Direct Calls", label_offset=(0.1, 0))
    draw_arrow(ax, (2.3, 2.4), (3.1, 1.4), label="Parameterized SQL", label_offset=(0, 0))
    draw_arrow(ax, (5.1, 2.4), (6.9, 1.4), label="Audit Commits (WAL)", label_offset=(0, 0))

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "fig_3_1_architecture.png")
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print("Generated", out)


# ================= 2. FIGURE 4.1: ACTIVITY DIAGRAM - DATA ENGINEERING =================
def generate_data_engineering_diagram():
    fig, ax = plt.subplots(figsize=(6.5, 8.5), dpi=300)
    ax.set_xlim(0, 6.5)
    ax.set_ylim(0, 9.5)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(3.25, 9.1, "Activity Diagram: Data Engineering", ha="center", va="center", fontsize=13, fontweight="bold", color="#0F172A")

    # Start Node
    start_circle = patches.Circle((3.25, 8.5), 0.22, facecolor="#0F172A", edgecolor="#0F172A", zorder=3)
    ax.add_patch(start_circle)
    ax.text(3.25, 8.85, "Start", ha="center", va="center", fontsize=9, fontweight="bold", color="#0F172A")

    # Steps
    draw_rounded_box(ax, (1.5, 7.3), 3.5, 0.7, "Open Product Registration Form", facecolor="#EFF6FF", edgecolor="#1D4ED8")
    draw_rounded_box(ax, (1.2, 6.0), 4.1, 0.8, "Enter Product Name, Category, Stock Qty,\nUnit Price, Expiry Date & Min Threshold", facecolor="#EFF6FF", edgecolor="#1D4ED8", fontsize=9)
    
    # Decision Diamond
    diamond = patches.Polygon([[3.25, 5.2], [4.6, 4.6], [3.25, 4.0], [1.9, 4.6]], closed=True, facecolor="#FEF3C7", edgecolor="#D97706", lw=1.8, zorder=3)
    ax.add_patch(diamond)
    ax.text(3.25, 4.6, "Validate\nInput?", ha="center", va="center", fontsize=9, fontweight="bold", color="#92400e")

    # Invalid branch
    draw_rounded_box(ax, (0.2, 3.2), 2.2, 0.7, "Display Validation\nError Message", facecolor="#FEE2E2", edgecolor="#DC2626", fontsize=8.5)

    # Valid branch
    draw_rounded_box(ax, (2.6, 2.7), 3.5, 0.8, "Execute Parameterized SQL INSERT\n(Auto-increment ID, Timestamps)", facecolor="#EFF6FF", edgecolor="#1D4ED8", fontsize=9)
    draw_rounded_box(ax, (2.6, 1.4), 3.5, 0.7, "Append 'ADD' to System Audit Log\n& Refresh Inventory Catalog", facecolor="#F0FDF4", edgecolor="#16A34A", fontsize=9)

    # End Node
    end_circle_outer = patches.Circle((4.35, 0.45), 0.25, facecolor="#FFFFFF", edgecolor="#0F172A", lw=2, zorder=3)
    end_circle_inner = patches.Circle((4.35, 0.45), 0.16, facecolor="#0F172A", edgecolor="#0F172A", zorder=4)
    ax.add_patch(end_circle_outer)
    ax.add_patch(end_circle_inner)
    ax.text(4.35, 0.1, "End", ha="center", va="center", fontsize=9, fontweight="bold", color="#0F172A")

    # Arrows
    draw_arrow(ax, (3.25, 8.28), (3.25, 8.0))
    draw_arrow(ax, (3.25, 7.3), (3.25, 6.8))
    draw_arrow(ax, (3.25, 6.0), (3.25, 5.2))
    
    # Diamond to invalid
    draw_arrow(ax, (1.9, 4.6), (1.3, 3.9), label="Invalid", label_offset=(-0.1, 0.2))
    # Invalid back up
    ax.annotate("", xy=(1.2, 6.4), xytext=(1.3, 3.2),
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color="#DC2626", lw=1.5,
                                connectionstyle="arc3,rad=-0.4"))

    # Diamond to valid
    draw_arrow(ax, (3.25, 4.0), (3.25, 3.5), label="Valid", label_offset=(0.3, 0))
    draw_arrow(ax, (4.35, 2.7), (4.35, 2.1))
    draw_arrow(ax, (4.35, 1.4), (4.35, 0.75))

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "fig_4_1_data_engineering.png")
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print("Generated", out)


# ================= 3. FIGURE 4.2: ACTIVITY DIAGRAM - CLOUD / DEPLOYMENT =================
def generate_cloud_engineering_diagram():
    fig, ax = plt.subplots(figsize=(6.5, 8.5), dpi=300)
    ax.set_xlim(0, 6.5)
    ax.set_ylim(0, 9.5)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(3.25, 9.1, "Activity Diagram: Cloud / Deployment Engineering", ha="center", va="center", fontsize=13, fontweight="bold", color="#0F172A")

    # Start Node
    start_circle = patches.Circle((3.25, 8.5), 0.22, facecolor="#0F172A", edgecolor="#0F172A", zorder=3)
    ax.add_patch(start_circle)
    ax.text(3.25, 8.85, "Start", ha="center", va="center", fontsize=9, fontweight="bold", color="#0F172A")

    draw_rounded_box(ax, (1.5, 7.3), 3.5, 0.7, "Prepare Project Source Files\n& dependencies (requirements.txt)", facecolor="#EFF6FF", edgecolor="#1D4ED8", fontsize=9)
    draw_rounded_box(ax, (1.5, 6.1), 3.5, 0.7, "Configure Environment\n(Python 3.11, FastAPI, Uvicorn)", facecolor="#EFF6FF", edgecolor="#1D4ED8", fontsize=9)

    # Decision Diamond: Mode
    diamond = patches.Polygon([[3.25, 5.4], [4.6, 4.8], [3.25, 4.2], [1.9, 4.8]], closed=True, facecolor="#FEF3C7", edgecolor="#D97706", lw=1.8, zorder=3)
    ax.add_patch(diamond)
    ax.text(3.25, 4.8, "Deployment\nMode?", ha="center", va="center", fontsize=9, fontweight="bold", color="#92400e")

    # Local Branch
    draw_rounded_box(ax, (0.3, 3.2), 2.7, 0.8, "Local Execution (Port 5000)\nUvicorn ASGI Server\n& Background Streamlit (8501)", facecolor="#EFF6FF", edgecolor="#1D4ED8", fontsize=8.5)

    # Cloud Branch
    draw_rounded_box(ax, (3.5, 3.2), 2.7, 0.8, "Cloud Web Service\n(Container / Streamlit Cloud)\nPersistent Disk Storage", facecolor="#F0FDF4", edgecolor="#16A34A", fontsize=8.5)

    draw_rounded_box(ax, (1.5, 1.7), 3.5, 0.8, "Open Web Browser & Verify Access\nCheck REST /docs & Live Catalog Sync", facecolor="#EFF6FF", edgecolor="#1D4ED8", fontsize=9)

    # End Node
    end_circle_outer = patches.Circle((3.25, 0.55), 0.25, facecolor="#FFFFFF", edgecolor="#0F172A", lw=2, zorder=3)
    end_circle_inner = patches.Circle((3.25, 0.55), 0.16, facecolor="#0F172A", edgecolor="#0F172A", zorder=4)
    ax.add_patch(end_circle_outer)
    ax.add_patch(end_circle_inner)
    ax.text(3.25, 0.2, "End", ha="center", va="center", fontsize=9, fontweight="bold", color="#0F172A")

    # Connecting arrows
    draw_arrow(ax, (3.25, 8.28), (3.25, 8.0))
    draw_arrow(ax, (3.25, 7.3), (3.25, 6.8))
    draw_arrow(ax, (3.25, 6.1), (3.25, 5.4))
    draw_arrow(ax, (2.3, 4.4), (1.65, 4.0), label="Local", label_offset=(-0.1, 0.15))
    draw_arrow(ax, (4.2, 4.4), (4.85, 4.0), label="Cloud", label_offset=(0.1, 0.15))
    draw_arrow(ax, (1.65, 3.2), (2.5, 2.5))
    draw_arrow(ax, (4.85, 3.2), (4.0, 2.5))
    draw_arrow(ax, (3.25, 1.7), (3.25, 0.85))

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "fig_4_2_cloud_engineering.png")
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print("Generated", out)


# ================= 4. FIGURE 4.3: ACTIVITY DIAGRAM - AI / RULE-BASED =================
def generate_ai_engineering_diagram():
    fig, ax = plt.subplots(figsize=(6.5, 9.0), dpi=300)
    ax.set_xlim(0, 6.5)
    ax.set_ylim(0, 10.0)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(3.25, 9.6, "Activity Diagram: AI Engineering (Rule-Based Alerts)", ha="center", va="center", fontsize=12.5, fontweight="bold", color="#0F172A")

    start_circle = patches.Circle((3.25, 9.05), 0.22, facecolor="#0F172A", edgecolor="#0F172A", zorder=3)
    ax.add_patch(start_circle)
    ax.text(3.25, 9.4, "Start", ha="center", va="center", fontsize=9, fontweight="bold", color="#0F172A")

    draw_rounded_box(ax, (1.5, 7.9), 3.5, 0.7, "Fetch Product Records from SQLite\n(Query products Table)", facecolor="#EFF6FF", edgecolor="#1D4ED8", fontsize=9)
    draw_rounded_box(ax, (1.5, 6.8), 3.5, 0.7, "Read System Local Date (date.today())\n& Calculate Expiry Deltas (Days Remaining)", facecolor="#EFF6FF", edgecolor="#1D4ED8", fontsize=9)

    # Expiry Check Diamond
    diamond_exp = patches.Polygon([[3.25, 6.2], [4.6, 5.6], [3.25, 5.0], [1.9, 5.6]], closed=True, facecolor="#FEF3C7", edgecolor="#D97706", lw=1.8, zorder=3)
    ax.add_patch(diamond_exp)
    ax.text(3.25, 5.6, "Evaluate\nExpiry?", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#92400e")

    # Expiry outcomes
    draw_rounded_box(ax, (0.2, 4.1), 1.8, 0.7, "Expired (< 0d)\nImmediate Disposal", facecolor="#FEE2E2", edgecolor="#DC2626", fontsize=8)
    draw_rounded_box(ax, (2.35, 4.1), 1.8, 0.7, "Expiring Soon (≤ 7d)\nMarkdown Candidate", facecolor="#FEF3C7", edgecolor="#D97706", fontsize=8)
    draw_rounded_box(ax, (4.5, 4.1), 1.8, 0.7, "Stable (OK / N/A)\nFresh / Non-Perishable", facecolor="#DCFCE7", edgecolor="#16A34A", fontsize=8)

    # Stock Check
    draw_rounded_box(ax, (1.2, 2.7), 4.1, 0.8, "Evaluate Stock Levels vs Minimum Threshold\nQuantity == 0 -> Out of Stock\n0 < Quantity <= Min Stock -> Low Stock Alert", facecolor="#EFF6FF", edgecolor="#1D4ED8", fontsize=9)

    draw_rounded_box(ax, (1.2, 1.4), 4.1, 0.8, "Compute Financial Valuation & Summary Metrics\nRender KPI Cards, Charts & Alert Hub Tables", facecolor="#F0FDF4", edgecolor="#16A34A", fontsize=9)

    # End Node
    end_circle_outer = patches.Circle((3.25, 0.55), 0.25, facecolor="#FFFFFF", edgecolor="#0F172A", lw=2, zorder=3)
    end_circle_inner = patches.Circle((3.25, 0.55), 0.16, facecolor="#0F172A", edgecolor="#0F172A", zorder=4)
    ax.add_patch(end_circle_outer)
    ax.add_patch(end_circle_inner)
    ax.text(3.25, 0.2, "End", ha="center", va="center", fontsize=9, fontweight="bold", color="#0F172A")

    # Connectors
    draw_arrow(ax, (3.25, 8.83), (3.25, 8.6))
    draw_arrow(ax, (3.25, 7.9), (3.25, 7.5))
    draw_arrow(ax, (3.25, 6.8), (3.25, 6.2))
    
    draw_arrow(ax, (2.2, 5.2), (1.1, 4.8), label="< 0d", label_offset=(-0.1, 0.15))
    draw_arrow(ax, (3.25, 5.0), (3.25, 4.8), label="≤ 7d", label_offset=(0.25, 0))
    draw_arrow(ax, (4.3, 5.2), (5.4, 4.8), label="> 7d", label_offset=(0.1, 0.15))

    draw_arrow(ax, (1.1, 4.1), (2.0, 3.5))
    draw_arrow(ax, (3.25, 4.1), (3.25, 3.5))
    draw_arrow(ax, (5.4, 4.1), (4.5, 3.5))

    draw_arrow(ax, (3.25, 2.7), (3.25, 2.2))
    draw_arrow(ax, (3.25, 1.4), (3.25, 0.85))

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "fig_4_3_ai_engineering.png")
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print("Generated", out)


# ================= 5. FIGURE 4.4: ACTIVITY DIAGRAM - SECURITY ENGINEERING =================
def generate_security_engineering_diagram():
    fig, ax = plt.subplots(figsize=(6.5, 8.5), dpi=300)
    ax.set_xlim(0, 6.5)
    ax.set_ylim(0, 9.5)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    ax.text(3.25, 9.1, "Activity Diagram: Security & Data Integrity", ha="center", va="center", fontsize=13, fontweight="bold", color="#0F172A")

    # Start Node
    start_circle = patches.Circle((3.25, 8.5), 0.22, facecolor="#0F172A", edgecolor="#0F172A", zorder=3)
    ax.add_patch(start_circle)
    ax.text(3.25, 8.85, "Start", ha="center", va="center", fontsize=9, fontweight="bold", color="#0F172A")

    draw_rounded_box(ax, (1.5, 7.3), 3.5, 0.7, "User Submits Catalog Request\n(Add, Edit, or Delete SKU)", facecolor="#EFF6FF", edgecolor="#1D4ED8", fontsize=9)
    draw_rounded_box(ax, (1.2, 6.0), 4.1, 0.8, "Server-Side Input Validation\nCheck non-empty fields, non-negative quantity\nand positive unit pricing in FastAPI / Pydantic", facecolor="#EFF6FF", edgecolor="#1D4ED8", fontsize=8.5)

    # Validation Diamond
    diamond = patches.Polygon([[3.25, 5.2], [4.6, 4.6], [3.25, 4.0], [1.9, 4.6]], closed=True, facecolor="#FEF3C7", edgecolor="#D97706", lw=1.8, zorder=3)
    ax.add_patch(diamond)
    ax.text(3.25, 4.6, "Validation\nPassed?", ha="center", va="center", fontsize=9, fontweight="bold", color="#92400e")

    # Fail
    draw_rounded_box(ax, (0.2, 3.2), 2.3, 0.7, "Reject Request\nReturn HTTP 400 Safe Message\n(No credentials exposed)", facecolor="#FEE2E2", edgecolor="#DC2626", fontsize=8)

    # Pass
    draw_rounded_box(ax, (2.6, 2.7), 3.5, 0.8, "Execute Parameterized SQL Query\n(100% Parameter Placeholders '?')\nPrevents SQL Injection Attacks", facecolor="#EFF6FF", edgecolor="#1D4ED8", fontsize=8.5)
    draw_rounded_box(ax, (2.6, 1.4), 3.5, 0.7, "Commit Transaction (WAL Mode)\nAppend Immutable Entry to audit_log Table", facecolor="#F0FDF4", edgecolor="#16A34A", fontsize=8.5)

    # End Node
    end_circle_outer = patches.Circle((4.35, 0.45), 0.25, facecolor="#FFFFFF", edgecolor="#0F172A", lw=2, zorder=3)
    end_circle_inner = patches.Circle((4.35, 0.45), 0.16, facecolor="#0F172A", edgecolor="#0F172A", zorder=4)
    ax.add_patch(end_circle_outer)
    ax.add_patch(end_circle_inner)
    ax.text(4.35, 0.1, "End", ha="center", va="center", fontsize=9, fontweight="bold", color="#0F172A")

    # Connectors
    draw_arrow(ax, (3.25, 8.28), (3.25, 8.0))
    draw_arrow(ax, (3.25, 7.3), (3.25, 6.8))
    draw_arrow(ax, (3.25, 6.0), (3.25, 5.2))
    
    draw_arrow(ax, (1.9, 4.6), (1.35, 3.9), label="Failed", label_offset=(-0.1, 0.2))
    draw_arrow(ax, (3.25, 4.0), (3.25, 3.5), label="Passed", label_offset=(0.3, 0))

    draw_arrow(ax, (4.35, 2.7), (4.35, 2.1))
    draw_arrow(ax, (4.35, 1.4), (4.35, 0.75))

    # Reject arrow to end
    draw_arrow(ax, (1.35, 3.2), (3.5, 0.7), label="Halt", label_offset=(-0.2, 0))

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "fig_4_4_security_engineering.png")
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print("Generated", out)


if __name__ == "__main__":
    generate_architecture_diagram()
    generate_data_engineering_diagram()
    generate_cloud_engineering_diagram()
    generate_ai_engineering_diagram()
    generate_security_engineering_diagram()
    print("All 5 diagrams generated successfully!")
