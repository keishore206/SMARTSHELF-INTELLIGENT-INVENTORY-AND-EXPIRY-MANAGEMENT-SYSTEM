"""
pages/inventory.py  -  SmartShelf
Searchable, filterable catalog with item inspector and status tracking.
"""

import streamlit as st
import pandas as pd

import database as db
import inventory_logic as logic
import styles

styles.page_header(
    "Inventory Catalog",
    "Filter, search, and inspect all inventory units currently registered in the database.",
)

# Search & Filter Controls
with st.container():
    f_col1, f_col2, f_col3, f_col4 = st.columns([3, 2, 2, 2])
    with f_col1:
        query = st.text_input("Search Products", placeholder="Enter product name...")
    with f_col2:
        db_cats = db.get_categories()
        category_options = ["All Categories"] + db_cats
        selected_category = st.selectbox("Category", category_options)
    with f_col3:
        stock_filter = st.selectbox(
            "Stock Status",
            ["All Levels", "In Stock", "Low Stock", "Out of Stock"],
        )
    with f_col4:
        expiry_filter = st.selectbox(
            "Expiry Status",
            ["All Lifecycles", "OK", "Expiring Soon", "Expired", "N/A"],
        )

# Fetch and enrich
db_cat_query = "" if selected_category == "All Categories" else selected_category
raw_results = db.search_products(query=query, category=db_cat_query)
enriched = logic.enrich_products(raw_results)

# Apply remaining in-memory filters
if stock_filter != "All Levels":
    enriched = [p for p in enriched if p.get("stock_status") == stock_filter]

if expiry_filter != "All Lifecycles":
    enriched = [p for p in enriched if p.get("expiry_status") == expiry_filter]

# Sorting controls
sort_col1, sort_col2 = st.columns([3, 1])
with sort_col2:
    sort_choice = st.selectbox(
        "Sort By",
        ["Name (A-Z)", "Quantity (High to Low)", "Quantity (Low to High)", "Unit Price (High to Low)", "Expiry Date (Earliest)"],
    )

if sort_choice == "Name (A-Z)":
    enriched.sort(key=lambda x: str(x.get("name", "")).lower())
elif sort_choice == "Quantity (High to Low)":
    enriched.sort(key=lambda x: int(x.get("quantity", 0)), reverse=True)
elif sort_choice == "Quantity (Low to High)":
    enriched.sort(key=lambda x: int(x.get("quantity", 0)))
elif sort_choice == "Unit Price (High to Low)":
    enriched.sort(key=lambda x: float(x.get("unit_price", 0.0)), reverse=True)
elif sort_choice == "Expiry Date (Earliest)":
    enriched.sort(key=lambda x: (x.get("expiry_date") is None, x.get("expiry_date") or ""))

total_in_db = db.get_dashboard_stats()["total_products"]
st.caption(f"Displaying {len(enriched)} of {total_in_db} total product(s) registered.")

if not enriched:
    styles.callout("No products match the selected criteria or search term.", kind="info")
else:
    # Prepare display DataFrame
    df_display = pd.DataFrame(enriched)
    columns_map = {
        "id": "ID",
        "name": "Product Name",
        "category": "Category",
        "quantity": "Quantity",
        "unit_price": "Price (Rs)",
        "expiry_date": "Expiry Date",
        "min_stock": "Min Threshold",
        "stock_status": "Stock Status",
        "expiry_status": "Expiry Status",
        "days_until_expiry": "Days Left",
    }
    cols_to_use = [k for k in columns_map.keys() if k in df_display.columns]
    df_view = df_display[cols_to_use].rename(columns=columns_map)

    # Format prices and empty fields
    df_view["Price (Rs)"] = df_view["Price (Rs)"].apply(lambda p: f"{float(p):,.2f}")
    df_view["Expiry Date"] = df_view["Expiry Date"].fillna("Not Specified")
    df_view["Days Left"] = df_view["Days Left"].apply(lambda d: "-" if pd.isna(d) else f"{int(d)} days")

    st.dataframe(df_view, use_container_width=True, hide_index=True)

    # Detail Inspector
    st.markdown("---")
    st.subheader("Item Specification Inspector")
    inspector_options = {f"#{p['id']} - {p['name']} ({p['category']})": p for p in enriched}
    selected_label = st.selectbox("Select product to view full record", list(inspector_options.keys()))
    selected_item = inspector_options[selected_label]

    item_val = float(selected_item.get("quantity", 0)) * float(selected_item.get("unit_price", 0.0))
    inspector_fields = {
        "Product Identification": f"#{selected_item.get('id')} - {selected_item.get('name')}",
        "Category Classification": str(selected_item.get("category")),
        "Stock Volume": f"{selected_item.get('quantity')} units (Threshold: {selected_item.get('min_stock')} units)",
        "Unit Cost / Total Value": f"Rs {float(selected_item.get('unit_price', 0)):,.2f} per unit  |  Total Inventory Value: Rs {item_val:,.2f}",
        "Stock Condition": str(selected_item.get("stock_status")),
        "Expiry Lifecycle": f"{selected_item.get('expiry_status')} (Expiry Date: {selected_item.get('expiry_date') or 'None'})",
        "Record Timestamps": f"Created: {selected_item.get('created_at', 'N/A')}  |  Updated: {selected_item.get('updated_at', 'N/A')}",
    }
    styles.detail_card(inspector_fields)
