"""
pages/reports.py  -  SmartShelf
Inventory summary reporting and CSV data export functionality.
"""

from datetime import date
import streamlit as st
import pandas as pd

import database as db
import inventory_logic as logic
import reports
import styles

styles.page_header(
    "Reports & Data Export",
    "Generate operational summaries and download complete inventory datasets for external audit or analysis.",
)

all_raw = db.get_all_products()
enriched = logic.enrich_products(all_raw)

if not enriched:
    styles.callout("No inventory records found in the system. Add items before generating reports.", kind="info")
else:
    # Key Summary Metrics
    total_val = sum(float(p.get("quantity", 0)) * float(p.get("unit_price", 0.0)) for p in enriched)
    total_units = sum(int(p.get("quantity", 0)) for p in enriched)
    avg_price = (total_val / total_units) if total_units > 0 else 0.0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Catalog SKUs", str(len(enriched)))
    col2.metric("Total Physical Units", f"{total_units:,}")
    col3.metric("Gross Valuation", f"Rs {total_val:,.2f}")
    col4.metric("Weighted Unit Value", f"Rs {avg_price:,.2f}")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    sec_summary, sec_export = st.columns([1, 1])

    with sec_summary:
        st.subheader("Executive Text Summary")
        summary_text = reports.build_summary(enriched)
        st.text_area(
            "Inventory Status Report",
            summary_text,
            height=260,
            disabled=True,
            label_visibility="collapsed",
        )

    with sec_export:
        st.subheader("Data Export")
        st.write("Download full inventory records with computed lifecycle states, values, and alert flags.")

        export_mode = st.radio(
            "Export Scope",
            ["Full Catalog", "Exceptions Only (Expired, Soon, or Low)"],
            horizontal=True,
        )

        if export_mode == "Full Catalog":
            export_data = enriched
        else:
            export_data = [
                p for p in enriched
                if p.get("expiry_status") in ("Expired", "Expiring Soon")
                or p.get("stock_status") in ("Low Stock", "Out of Stock")
            ]

        csv_bytes = reports.products_to_csv(export_data)
        today_stamp = date.today().isoformat()
        file_suffix = "exceptions" if export_mode != "Full Catalog" else "full"
        file_name = f"smartshelf_inventory_{file_suffix}_{today_stamp}.csv"

        st.caption(f"Ready to export {len(export_data)} record(s) in CSV format.")
        st.download_button(
            label="Download CSV Report",
            data=csv_bytes,
            file_name=file_name,
            mime="text/csv",
            type="primary",
        )

    st.markdown("---")
    st.subheader("Export Preview Dataset")
    if export_data:
        df_preview = pd.DataFrame(export_data)[
            ["id", "name", "category", "quantity", "unit_price", "expiry_date", "stock_status", "expiry_status"]
        ]
        df_preview.columns = [
            "ID", "Name", "Category", "Quantity", "Unit Price (Rs)", "Expiry Date", "Stock Status", "Expiry Status"
        ]
        df_preview["Unit Price (Rs)"] = df_preview["Unit Price (Rs)"].apply(lambda p: f"{float(p):,.2f}")
        st.dataframe(df_preview, use_container_width=True, hide_index=True)
