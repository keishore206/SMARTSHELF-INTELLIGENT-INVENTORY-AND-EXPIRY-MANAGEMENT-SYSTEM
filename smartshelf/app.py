"""
app.py  -  SmartShelf
Navigation controller and application entry point.
Run with: streamlit run app.py
"""

import sys
import os

# Ensure project root is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import database as db
import styles

st.set_page_config(
    page_title="SmartShelf - Inventory Platform",
    layout="wide",
    initial_sidebar_state="expanded",
)

styles.apply_styles()
styles.sidebar_brand()
db.init_db()

# Navigation definition with sections and clean titles (no emoji)
pg = st.navigation(
    {
        "Overview": [
            st.Page("pages/dashboard.py", title="Dashboard", default=True),
        ],
        "Inventory": [
            st.Page("pages/inventory.py", title="Inventory Catalog"),
            st.Page("pages/add_product.py", title="Add Product"),
            st.Page("pages/edit_product.py", title="Edit Product"),
            st.Page("pages/delete_product.py", title="Delete Product"),
        ],
        "Monitoring": [
            st.Page("pages/alerts.py", title="Alerts & Exceptions"),
            st.Page("pages/reports.py", title="Reports & Export"),
        ],
        "System": [
            st.Page("pages/audit_log.py", title="System Audit Log"),
        ],
    }
)

pg.run()
