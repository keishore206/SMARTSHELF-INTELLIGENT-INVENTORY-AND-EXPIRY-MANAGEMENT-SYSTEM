"""
pages/edit_product.py  -  SmartShelf
Modify attributes, adjust stock counts, or update thresholds for existing products.
"""

from datetime import datetime, date
import streamlit as st

import database as db
import styles

styles.page_header(
    "Edit Product Record",
    "Update stock counts, unit pricing, categories, and lifecycle dates for existing items.",
)

all_products = db.get_all_products()

if not all_products:
    styles.callout("No products found in the database. Please add products first.", kind="info")
else:
    options = {f"#{p['id']} - {p['name']} ({p['category']})": p["id"] for p in all_products}
    selected_label = st.selectbox("Select product to modify", list(options.keys()))
    product_id = options[selected_label]
    current = db.get_product_by_id(product_id)

    if current:
        edit_col, info_col = st.columns([3, 2])

        with edit_col:
            with st.form("edit_form"):
                st.subheader("Edit Parameters")
                new_name = st.text_input("Product Name *", value=current["name"])
                new_category = st.text_input("Category *", value=current["category"])

                q_c, p_c = st.columns(2)
                with q_c:
                    new_qty = st.number_input("Quantity *", min_value=0, step=1, value=int(current["quantity"]))
                with p_c:
                    new_price = st.number_input(
                        "Unit Price (Rs) *",
                        min_value=0.0,
                        step=0.5,
                        value=float(current["unit_price"]),
                    )

                st.markdown("---")
                has_exp_currently = bool(current.get("expiry_date"))
                has_expiry = st.checkbox("Track Expiry Date", value=has_exp_currently)

                new_expiry = None
                if has_expiry:
                    default_date = date.today()
                    if current.get("expiry_date"):
                        try:
                            default_date = datetime.strptime(current["expiry_date"], "%Y-%m-%d").date()
                        except ValueError:
                            default_date = date.today()
                    new_expiry = st.date_input("Expiry Date", value=default_date)

                new_min_stock = st.number_input(
                    "Minimum Stock Alert Threshold",
                    min_value=0,
                    step=1,
                    value=int(current.get("min_stock", 5)),
                )

                submit_btn = st.form_submit_button("Save Product Changes", type="primary")

                if submit_btn:
                    errors = []
                    if not new_name.strip():
                        errors.append("Product name is required.")
                    if not new_category.strip():
                        errors.append("Category is required.")
                    if new_price < 0:
                        errors.append("Unit price must be non-negative.")
                    if new_qty < 0:
                        errors.append("Quantity must be non-negative.")

                    if errors:
                        for err in errors:
                            styles.callout(err, kind="danger")
                    else:
                        exp_str = new_expiry.isoformat() if has_expiry and new_expiry else None
                        success = db.update_product(
                            product_id=product_id,
                            name=new_name.strip(),
                            category=new_category.strip(),
                            quantity=new_qty,
                            unit_price=new_price,
                            expiry_date=exp_str,
                            min_stock=new_min_stock,
                        )
                        if success:
                            styles.callout(
                                f"Product #{product_id} ('{new_name.strip()}') was successfully updated.",
                                kind="success",
                            )
                        else:
                            styles.callout("Update could not be completed. Item might have been removed.", kind="danger")

        with info_col:
            st.subheader("Current Database Record")
            current_val = float(current.get("quantity", 0)) * float(current.get("unit_price", 0.0))
            record_info = {
                "Internal ID": f"#{current['id']}",
                "Product Name": current["name"],
                "Category": current["category"],
                "Quantity On Hand": f"{current['quantity']} units",
                "Unit Price": f"Rs {float(current['unit_price']):,.2f}",
                "Inventory Valuation": f"Rs {current_val:,.2f}",
                "Current Expiry Date": current.get("expiry_date") or "None",
                "Minimum Threshold": f"{current.get('min_stock', 5)} units",
                "Last Updated": current.get("updated_at", "N/A"),
            }
            styles.detail_card(record_info)
