"""
pages/audit_log.py  -  SmartShelf
Immutable chronological event journal of all database mutations.
"""

import streamlit as st
import pandas as pd

import database as db
import styles

styles.page_header(
    "System Audit Log",
    "Chronological event ledger recording all catalog additions, modifications, and deletions for governance and traceability.",
)

# Filter controls
col_action, col_limit, col_query = st.columns([2, 1, 3])

with col_action:
    action_filter = st.selectbox("Action Type", ["All Actions", "ADD", "EDIT", "DELETE"])

with col_limit:
    limit_choice = st.selectbox("Row Limit", [50, 100, 200, 500], index=1)

with col_query:
    search_query = st.text_input("Search Log Details", placeholder="Search by text or product ID...")

raw_logs = db.get_audit_log(limit=limit_choice)

if not raw_logs:
    styles.callout("No audit log events recorded in the database.", kind="info")
else:
    # Filter by action
    filtered = raw_logs
    if action_filter != "All Actions":
        filtered = [l for l in filtered if l.get("action") == action_filter]

    # Filter by query
    if search_query.strip():
        q = search_query.strip().lower()
        filtered = [
            l for l in filtered
            if q in str(l.get("details", "")).lower() or q in str(l.get("product_id", "")).lower()
        ]

    # Metrics Summary
    total_logged = len(raw_logs)
    count_adds = sum(1 for l in raw_logs if l.get("action") == "ADD")
    count_edits = sum(1 for l in raw_logs if l.get("action") == "EDIT")
    count_deletes = sum(1 for l in raw_logs if l.get("action") == "DELETE")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Events Logged", str(total_logged))
    m2.metric("Products Added", str(count_adds))
    m3.metric("Product Edits", str(count_edits))
    m4.metric("Product Deletions", str(count_deletes))

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
    st.caption(f"Showing {len(filtered)} matching event(s) out of {total_logged} most recent entries.")

    if filtered:
        df_log = pd.DataFrame(filtered)[["id", "timestamp", "action", "product_id", "details"]]
        df_log.columns = ["Event ID", "Timestamp", "Action", "Product ID", "Details"]
        df_log["Product ID"] = df_log["Product ID"].apply(lambda pid: f"#{pid}" if pd.notna(pid) else "N/A")
        st.dataframe(df_log, use_container_width=True, hide_index=True)
    else:
        styles.callout("No audit log events match the current filter criteria.", kind="info")
