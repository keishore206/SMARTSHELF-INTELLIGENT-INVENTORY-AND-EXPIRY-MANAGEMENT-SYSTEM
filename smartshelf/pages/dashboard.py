"""
pages/dashboard.py  -  SmartShelf
Executive overview: KPIs, category breakdown, stock health, and expiry timeline.
"""

import streamlit as st
import pandas as pd
from datetime import date

import database as db
import inventory_logic as logic
import styles

styles.page_header(
    "Inventory Dashboard",
    f"Executive overview and real-time operational health. System date: {date.today().strftime('%B %d, %Y')}",
)

# Fetch data
raw_products = db.get_all_products()
stats = db.get_dashboard_stats()
enriched = logic.enrich_products(raw_products)
counts = logic.dashboard_counts(enriched)

# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Catalog SKUs", f"{stats['total_products']:,}")
col2.metric("Total Units", f"{stats['total_units']:,}")
col3.metric("Stock Valuation", f"Rs {stats['total_value']:,.2f}")
col4.metric("Expired Items", str(counts["expired"]))
col5.metric("Low Stock Alerts", str(counts["low_stock"]))

st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

# Status Callouts
if counts["expired"] > 0:
    styles.callout(
        f"Critical Notice: {counts['expired']} item(s) have passed their expiration date. Navigate to Alerts to review and take action.",
        kind="danger",
    )

if counts["low_stock"] > 0:
    styles.callout(
        f"Inventory Notice: {counts['low_stock']} item(s) have reached or fallen below minimum safe stock levels.",
        kind="warning",
    )

if counts["expired"] == 0 and counts["low_stock"] == 0 and len(enriched) > 0:
    styles.callout(
        "All shelf parameters are within optimal operational bounds.",
        kind="success",
    )

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# Visualizations
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Units by Category")
    if enriched:
        df_all = pd.DataFrame(enriched)
        cat_agg = df_all.groupby("category")["quantity"].sum().reset_index()
        cat_agg.columns = ["Category", "Total Units"]
        cat_agg = cat_agg.sort_values(by="Total Units", ascending=False)
        st.bar_chart(cat_agg.set_index("Category"), color="#1d4ed8")
    else:
        st.info("No catalog items registered. Add products to populate category analytics.")

with chart_col2:
    st.subheader("Stock Health Breakdown")
    if enriched:
        df_all = pd.DataFrame(enriched)
        health_counts = df_all["stock_status"].value_counts().reset_index()
        health_counts.columns = ["Status", "Count"]
        st.bar_chart(health_counts.set_index("Status"), color="#0f766e")
    else:
        st.info("No catalog items registered.")

st.markdown("---")

# Expiry Timeline (Next 30 Days)
st.subheader("Upcoming Expirations (Next 30 Days)")
if enriched:
    upcoming = [
        p for p in enriched
        if p.get("days_until_expiry") is not None and 0 <= p["days_until_expiry"] <= 30
    ]
    upcoming.sort(key=lambda x: x["days_until_expiry"])

    if upcoming:
        df_up = pd.DataFrame(upcoming)[
            ["name", "category", "quantity", "unit_price", "expiry_date", "days_until_expiry", "expiry_status"]
        ]
        df_up.columns = [
            "Product Name", "Category", "Current Quantity", "Unit Price (Rs)", "Expiry Date", "Days Remaining", "Status"
        ]
        st.dataframe(
            df_up,
            use_container_width=True,
            hide_index=True,
        )
    else:
        styles.callout("No products are scheduled to expire in the upcoming 30 days.", kind="info")
else:
    st.info("Add products with expiration dates to monitor the shelf lifecycle.")
