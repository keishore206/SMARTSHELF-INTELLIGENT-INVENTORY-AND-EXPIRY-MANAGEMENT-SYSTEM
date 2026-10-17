"""
pages/delete_product.py  -  SmartShelf
Safely remove products from catalog with safety confirmation and audit recording.
"""

import streamlit as st

import database as db
import styles

styles.page_header(
    "Delete Product",
    "Permanently remove an item from the catalog. All deletions are immutably logged to the audit log.",
)

all_products = db.get_all_products()

if not all_products:
    styles.callout("No products found in the database.", kind="info")
else:
    options = {f"#{p['id']} - {p['name']} ({p['category']})": p["id"] for p in all_products}
    selected_label = st.selectbox("Select product to remove", list(options.keys()))
    product_id = options[selected_label]
    p = db.get_product_by_id(product_id)

    if p:
        col_summary, col_action = st.columns([1, 1])

        with col_summary:
            st.subheader("Selected Item Summary")
            item_val = float(p.get("quantity", 0)) * float(p.get("unit_price", 0.0))
            summary_info = {
                "Product ID": f"#{p['id']}",
                "Product Name": p["name"],
                "Category": p["category"],
                "Stock Units": f"{p['quantity']} units",
                "Unit Price": f"Rs {float(p['unit_price']):,.2f}",
                "Total Loss/Write-off Valuation": f"Rs {item_val:,.2f}",
                "Expiry Date": p.get("expiry_date") or "Not applicable",
            }
            styles.detail_card(summary_info)

        with col_action:
            st.subheader("Confirmation & Deletion")
            styles.callout(
                f"Warning: Deleting '{p['name']}' will permanently remove it from inventory records and active reporting.",
                kind="danger",
            )

            st.write("To prevent accidental deletion, enter the exact product name below:")
            confirm_input = st.text_input("Confirm Product Name", placeholder=p["name"])
            ack_check = st.checkbox("I confirm that this item should be permanently deleted.")

            if st.button("Permanently Delete Product", type="primary"):
                if not ack_check:
                    styles.callout("Please mark the confirmation checkbox before proceeding.", kind="warning")
                elif confirm_input.strip().lower() != p["name"].strip().lower():
                    styles.callout("Entered product name does not match. Deletion aborted.", kind="danger")
                else:
                    success = db.delete_product(product_id)
                    if success:
                        styles.callout(
                            f"Product #{product_id} ('{p['name']}') was successfully deleted.",
                            kind="success",
                        )
                        st.rerun()
                    else:
                        styles.callout("Deletion failed. The record might have already been removed.", kind="danger")
