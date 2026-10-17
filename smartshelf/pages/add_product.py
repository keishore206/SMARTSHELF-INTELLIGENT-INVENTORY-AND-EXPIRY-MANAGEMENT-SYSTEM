"""
pages/add_product.py  -  SmartShelf
Register a new product with live validation and preview.
"""

from datetime import date
import streamlit as st

import database as db
import styles

styles.page_header(
    "Register New Product",
    "Enter product metadata, stock counts, valuation, and shelf life parameters.",
)

existing_categories = db.get_categories()

form_col, preview_col = st.columns([3, 2])

with form_col:
    with st.form("add_product_form", clear_on_submit=False):
        st.subheader("Product Details")
        name = st.text_input("Product Name *", placeholder="e.g. Whole Milk 1L")

        cat_col1, cat_col2 = st.columns(2)
        with cat_col1:
            category_mode = st.radio(
                "Category Mode",
                ["Choose Existing", "Create New"],
                horizontal=True,
                label_visibility="collapsed",
            )
        with cat_col2:
            if category_mode == "Choose Existing" and existing_categories:
                category = st.selectbox("Category *", existing_categories)
            else:
                category = st.text_input("New Category Name *", placeholder="e.g. Beverages")

        q_col, p_col = st.columns(2)
        with q_col:
            quantity = st.number_input("Initial Quantity *", min_value=0, step=1, value=10)
        with p_col:
            unit_price = st.number_input("Unit Price (Rs) *", min_value=0.0, step=0.5, value=25.0)

        st.markdown("---")
        st.subheader("Lifecycle & Thresholds")

        t_col1, t_col2 = st.columns(2)
        with t_col1:
            has_expiry = st.checkbox("Enable Expiration Tracking", value=True)
            expiry_val = None
            if has_expiry:
                expiry_val = st.date_input("Expiry Date", min_value=date.today())
        with t_col2:
            min_stock = st.number_input("Minimum Stock Alert Threshold", min_value=0, step=1, value=5)

        submit_btn = st.form_submit_button("Register Product", type="primary")

        if submit_btn:
            errors = []
            if not name.strip():
                errors.append("Product name is required.")
            if not category.strip():
                errors.append("Category is required.")
            if unit_price < 0:
                errors.append("Unit price must be non-negative.")
            if quantity < 0:
                errors.append("Quantity must be non-negative.")

            if errors:
                for err in errors:
                    styles.callout(err, kind="danger")
            else:
                exp_str = expiry_val.isoformat() if has_expiry and expiry_val else None
                pid = db.add_product(
                    name=name.strip(),
                    category=category.strip(),
                    quantity=quantity,
                    unit_price=unit_price,
                    expiry_date=exp_str,
                    min_stock=min_stock,
                )
                styles.callout(
                    f"Product '{name.strip()}' has been registered in the catalog with ID #{pid}.",
                    kind="success",
                )

with preview_col:
    st.subheader("Real-Time Card Preview")
    calc_val = float(quantity) * float(unit_price)
    preview_data = {
        "Product Name": name.strip() if name.strip() else "[Pending Input]",
        "Category": category.strip() if category.strip() else "[Unassigned]",
        "Quantity On Hand": f"{quantity} units",
        "Unit Cost": f"Rs {unit_price:,.2f}",
        "Batch Total Valuation": f"Rs {calc_val:,.2f}",
        "Expiration Date": str(expiry_val) if has_expiry and expiry_val else "None (Non-perishable)",
        "Minimum Safe Stock": f"{min_stock} units",
    }
    styles.detail_card(preview_data)
