"""
pages/alerts.py  -  SmartShelf
Exception monitoring: Expired stock, upcoming expirations (<7 days), and inventory deficits.
"""

import streamlit as st
import pandas as pd

import database as db
import inventory_logic as logic
import styles

styles.page_header(
    "Alerts & Exceptions",
    "Monitor inventory risks including expired batches, impending shelf expirations, and stock shortages.",
)

all_raw = db.get_all_products()
enriched = logic.enrich_products(all_raw)

expired_items = logic.filter_expired(enriched)
expiring_soon_items = logic.filter_expiring_soon(enriched)
low_stock_items = logic.filter_low_stock(enriched)

# Top Metric Cards
m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric("Expired Items", str(len(expired_items)))
m_col2.metric("Expiring Soon (< 7 Days)", str(len(expiring_soon_items)))
m_col3.metric("Stock Depletion Alerts", str(len(low_stock_items)))

st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

# Tabs
tab_expired, tab_soon, tab_low = st.tabs(["Expired Stock", "Expiring Soon", "Low & Depleted Stock"])

with tab_expired:
    if expired_items:
        loss_val = sum(float(p.get("quantity", 0)) * float(p.get("unit_price", 0.0)) for p in expired_items)
        styles.callout(
            f"Action Required: {len(expired_items)} item(s) are expired. Total potential loss value: Rs {loss_val:,.2f}.",
            kind="danger",
        )

        df_exp = pd.DataFrame(expired_items)[
            ["id", "name", "category", "quantity", "unit_price", "expiry_date", "days_until_expiry"]
        ]
        df_exp.columns = [
            "ID", "Product Name", "Category", "Quantity", "Unit Price (Rs)", "Expiry Date", "Days Expired"
        ]
        df_exp["Days Expired"] = df_exp["Days Expired"].apply(lambda d: f"{abs(int(d))} days ago")
        df_exp["Unit Price (Rs)"] = df_exp["Unit Price (Rs)"].apply(lambda p: f"{float(p):,.2f}")
        st.dataframe(df_exp, use_container_width=True, hide_index=True)
    else:
        styles.callout("No catalog items are expired. Zero shelf spoilage detected.", kind="success")

with tab_soon:
    if expiring_soon_items:
        styles.callout(
            f"Advisory: {len(expiring_soon_items)} item(s) are set to expire within {logic.EXPIRY_WARNING_DAYS} days. Consider priority sales or discount reallocation.",
            kind="warning",
        )

        df_soon = pd.DataFrame(expiring_soon_items)[
            ["id", "name", "category", "quantity", "unit_price", "expiry_date", "days_until_expiry"]
        ]
        df_soon.columns = [
            "ID", "Product Name", "Category", "Quantity", "Unit Price (Rs)", "Expiry Date", "Days Remaining"
        ]
        df_soon["Days Remaining"] = df_soon["Days Remaining"].apply(lambda d: f"{int(d)} day(s)")
        df_soon["Unit Price (Rs)"] = df_soon["Unit Price (Rs)"].apply(lambda p: f"{float(p):,.2f}")
        st.dataframe(df_soon, use_container_width=True, hide_index=True)
    else:
        styles.callout("No products are expiring within the immediate warning window.", kind="success")

with tab_low:
    if low_stock_items:
        styles.callout(
            f"Reorder Trigger: {len(low_stock_items)} item(s) are at or below minimum threshold. Initiate supplier replenishment orders.",
            kind="warning",
        )

        df_low = pd.DataFrame(low_stock_items)[
            ["id", "name", "category", "quantity", "min_stock", "unit_price", "stock_status"]
        ]
        df_low.columns = [
            "ID", "Product Name", "Category", "Current Stock", "Min Threshold", "Unit Price (Rs)", "Status"
        ]
        df_low["Unit Price (Rs)"] = df_low["Unit Price (Rs)"].apply(lambda p: f"{float(p):,.2f}")
        st.dataframe(df_low, use_container_width=True, hide_index=True)
    else:
        styles.callout("All catalog items maintain stock volume above minimum thresholds.", kind="success")
