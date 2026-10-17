"""
styles.py  -  SmartShelf
Shared CSS (Inter font, professional palette) injected on every page,
plus layout utility helpers.
"""

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    box-sizing: border-box;
}
.main { background: #f1f5f9; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1280px !important; }

/* Sidebar */
section[data-testid="stSidebar"] { background: #0f172a !important; border-right: 1px solid #1e293b !important; }
section[data-testid="stSidebar"] > div:first-child { background: #0f172a !important; }
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] li { color: #94a3b8 !important; }
section[data-testid="stSidebar"] a {
    color: #94a3b8 !important; font-weight: 500 !important; border-radius: 6px !important;
    padding: 0.35rem 0.6rem !important; display: block; text-decoration: none !important;
}
section[data-testid="stSidebar"] a:hover { color: #f1f5f9 !important; background: #1e293b !important; }
section[data-testid="stSidebar"] a[aria-current="page"] { color: #f1f5f9 !important; background: #1e3a5f !important; }

/* Typography */
h1 { font-weight:700 !important; font-size:1.6rem !important; color:#0f172a !important; letter-spacing:-0.02em !important; line-height:1.2 !important; margin:0 0 0.2rem 0 !important; }
h2 { font-weight:600 !important; font-size:1.15rem !important; color:#1e293b !important; }
h3 { font-weight:600 !important; font-size:0.95rem !important; color:#334155 !important; }
p  { color:#475569 !important; line-height:1.6 !important; }
label { font-weight:500 !important; font-size:0.85rem !important; color:#374151 !important; }

/* Page header card */
.page-hdr {
    background:#fff; border:1px solid #e2e8f0; border-left:4px solid #1d4ed8;
    border-radius:10px; padding:1.25rem 1.75rem; margin-bottom:1.75rem;
    box-shadow:0 1px 3px rgba(15,23,42,0.05);
}
.page-hdr h1 { margin:0 !important; }
.page-hdr .sub { color:#64748b !important; font-size:0.875rem !important; margin:0.3rem 0 0 0 !important; font-weight:400 !important; }

/* Metric cards */
div[data-testid="metric-container"] {
    background:#fff !important; border:1px solid #e2e8f0 !important; border-radius:10px !important;
    padding:1.2rem 1.4rem !important; box-shadow:0 1px 2px rgba(15,23,42,0.04) !important;
}
div[data-testid="stMetricLabel"] > div { font-size:0.72rem !important; font-weight:600 !important; color:#64748b !important; text-transform:uppercase !important; letter-spacing:0.07em !important; }
div[data-testid="stMetricValue"]       { font-size:2rem !important; font-weight:700 !important; color:#0f172a !important; letter-spacing:-0.03em !important; }

/* Buttons */
.stButton > button { font-family:'Inter',sans-serif !important; font-weight:500 !important; border-radius:7px !important; font-size:0.875rem !important; padding:0.5rem 1.25rem !important; transition:all 0.15s ease !important; }
.stButton > button[kind="primary"]   { background:#1d4ed8 !important; color:#fff !important; border:none !important; }
.stButton > button[kind="primary"]:hover { background:#1e40af !important; }
.stButton > button[kind="secondary"] { background:#fff !important; border:1px solid #e2e8f0 !important; color:#374151 !important; }
.stDownloadButton > button { background:#0f766e !important; color:#fff !important; border:none !important; border-radius:7px !important; font-weight:500 !important; }

/* Inputs */
.stTextInput input, .stNumberInput input, .stDateInput input { border-radius:7px !important; border-color:#e2e8f0 !important; font-size:0.9rem !important; color:#0f172a !important; }
.stSelectbox > div > div { border-radius:7px !important; border-color:#e2e8f0 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background:#f8fafc !important; border-radius:8px !important; padding:0.2rem !important; border:1px solid #e2e8f0 !important; gap:2px !important; }
.stTabs [data-baseweb="tab"] { border-radius:6px !important; padding:0.4rem 1.1rem !important; font-weight:500 !important; font-size:0.875rem !important; color:#64748b !important; border:none !important; background:transparent !important; }
.stTabs [aria-selected="true"] { background:#fff !important; color:#0f172a !important; box-shadow:0 1px 3px rgba(0,0,0,0.08) !important; }

/* Dataframe */
.stDataFrame { border:1px solid #e2e8f0 !important; border-radius:8px !important; }
iframe { border-radius:8px !important; }

/* Form */
.stForm { background:#fff !important; border:1px solid #e2e8f0 !important; border-radius:10px !important; padding:1.5rem !important; }

/* Misc */
hr { border-color:#e2e8f0 !important; margin:1.5rem 0 !important; }
.stAlert { border-radius:8px !important; }
.stCaption { color:#64748b !important; font-size:0.8rem !important; }
#MainMenu, footer { visibility:hidden !important; }
header[data-testid="stHeader"] { background:transparent !important; }

/* Callout boxes */
.callout { border-radius:8px; padding:0.9rem 1.2rem; font-size:0.875rem; line-height:1.55; margin-bottom:0.5rem; }
.callout-info    { background:#eff6ff; border:1px solid #bfdbfe; color:#1e40af; }
.callout-warning { background:#fffbeb; border:1px solid #fde68a; color:#92400e; }
.callout-danger  { background:#fef2f2; border:1px solid #fecaca; color:#991b1b; }
.callout-success { background:#f0fdf4; border:1px solid #bbf7d0; color:#15803d; }

/* Status Badges */
.badge { display:inline-block; padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:600; text-transform:uppercase; letter-spacing:0.04em; }
.badge-danger  { background:#fee2e2; color:#991b1b; border:1px solid #fecaca; }
.badge-warning { background:#fef3c7; color:#92400e; border:1px solid #fde68a; }
.badge-success { background:#dcfce7; color:#166534; border:1px solid #bbf7d0; }
.badge-neutral { background:#f1f5f9; color:#475569; border:1px solid #e2e8f0; }
.badge-info    { background:#eff6ff; color:#1e40af; border:1px solid #bfdbfe; }

/* Detail card */
.detail-card { background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:1.25rem 1.5rem; }
.detail-label { font-size:0.72rem; font-weight:600; color:#94a3b8; text-transform:uppercase; letter-spacing:0.07em; margin:0 0 0.15rem 0; }
.detail-value { font-size:1rem; font-weight:500; color:#0f172a; margin:0 0 1rem 0; }
</style>
"""


def apply_styles() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def sidebar_brand() -> None:
    st.sidebar.markdown(
        """
        <div style="padding:1.25rem 0.5rem 1rem 0.5rem;">
            <div style="color:#f1f5f9;font-size:1.1rem;font-weight:700;letter-spacing:-0.01em;">SmartShelf</div>
            <div style="color:#64748b;font-size:0.75rem;margin-top:0.15rem;font-weight:500;">Inventory Platform</div>
        </div>
        <hr style="border-color:#1e293b;margin:0 0 0.75rem 0;">
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str = "") -> None:
    sub = f'<p class="sub">{subtitle}</p>' if subtitle else ""
    st.markdown(f'<div class="page-hdr"><h1>{title}</h1>{sub}</div>', unsafe_allow_html=True)


def callout(message: str, kind: str = "info") -> None:
    """kind: info | warning | danger | success"""
    st.markdown(f'<div class="callout callout-{kind}">{message}</div>', unsafe_allow_html=True)


def badge(text: str, kind: str = "neutral") -> str:
    """kind: danger | warning | success | neutral | info"""
    return f'<span class="badge badge-{kind}">{text}</span>'


def detail_row(label: str, value: str) -> str:
    return f'<p class="detail-label">{label}</p><p class="detail-value">{value}</p>'


def detail_card(fields: dict) -> None:
    rows = "".join(detail_row(k, str(v)) for k, v in fields.items())
    st.markdown(f'<div class="detail-card">{rows}</div>', unsafe_allow_html=True)

