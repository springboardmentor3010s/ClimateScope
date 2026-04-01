import streamlit as st

def load_css():
    st.markdown("""
    <style>

    /* MAIN BACKGROUND */
    .stApp {
        background: linear-gradient(120deg,#eef2ff,#f0f9ff,#ecfeff);
    }

    /* HIDE STREAMLIT PAGE NAV */
    [data-testid="stSidebarNav"] {
        display: none;
    }

    /* KPI GLASS CARDS */

    .glass-card{
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(10px);
    padding:20px;
    border-radius:12px;
    box-shadow:0 4px 10px rgba(0,0,0,0.1);
}

    .glass-card.temp{
        border-left:6px solid #ef4444;
    }
                
    .glass-card.trend{
    border-left:6px solid #f97316;
    }

    .glass-card.rain{
        border-left:6px solid #3b82f6;
    }
    
    

    .glass-card.wind{
        border-left:6px solid #10b981;
    }

    .glass-card.humidity{
        border-left:6px solid #2563eb;
    }

    .glass-card.events{
        border-left:6px solid #f59e0b;
    }

    .glass-card:hover{
    transform: translateY(-4px);
    transition: 0.2s ease;
    }
    
    /* DATA SUMMARY CARDS */

    .summary-card{
        background: rgba(255,255,255,0.8);
        backdrop-filter: blur(10px);
        padding:16px;
        border-radius:12px;
        text-align:center;
        box-shadow:0 3px 8px rgba(0,0,0,0.08);
        border-left:5px solid #6366f1;
    }

    .summary-title{
        font-size:14px;
        color:#555;
        font-weight:600;
    }

    .summary-value{
        font-size:26px;
        font-weight:700;
        margin-top:5px;
    }

        .kpi-title{
            font-size:14px;
            color:#555;
            font-weight:600;
        }

    .kpi-value{
        font-size:28px;
        font-weight:700;
        margin-top:5px;
    }
    

    /* INSIGHT BOX */

    .insight-box{
        background:linear-gradient(135deg,#eef2ff,#e0f2fe);
        border-left:6px solid #6366f1;
        padding:20px;
        border-radius:12px;
        font-size:16px;
    }
    
    .insight-card{
    background: rgba(255,255,255,0.8);
    backdrop-filter: blur(8px);
    padding:16px;
    border-radius:10px;
    margin-bottom:12px;
    box-shadow:0 3px 8px rgba(0,0,0,0.08);
    border-left:5px solid #6366f1;
    }

    .insight-up{
        color:#16a34a;
        font-weight:600;
    }

    .insight-down{
        color:#dc2626;
        font-weight:600;
    }
                
    .hotspot-card{
    background: rgba(255,255,255,0.8);
    backdrop-filter: blur(8px);
    padding:12px;
    border-radius:10px;
    margin-bottom:10px;
    box-shadow:0 3px 6px rgba(0,0,0,0.08);
    border-left:5px solid #ef4444;
    }
                
    /* SIDEBAR BACKGROUND */

    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg,#e0e7ff,#c7d2fe,#a5b4fc);
    }
    

    /* Sidebar text color */

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] p {
        color:#1e293b !important;
    }

    /* Sidebar header */
    section[data-testid="stSidebar"] h2 {
        font-weight:700;
        color:#1e293b !important;
    }

    /* Sidebar widgets */

    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stMultiSelect,
    [data-testid="stSidebar"] .stSlider,
    [data-testid="stSidebar"] .stCheckbox {
        background:white;
        border-radius:10px;
        padding:4px;
        box-shadow:0 2px 6px rgba(0,0,0,0.05);
    }
                
    /* SIDEBAR HOVER EFFECTS */

    /* Hover highlight for widgets */
    section[data-testid="stSidebar"] .stSelectbox:hover,
    section[data-testid="stSidebar"] .stMultiSelect:hover,
    section[data-testid="stSidebar"] .stSlider:hover,
    section[data-testid="stSidebar"] .stCheckbox:hover {
        background:#f8fafc;
        border-radius:8px;
        transition:0.2s ease;
    }

    /* Active focus highlight */
    section[data-testid="stSidebar"] .stSelectbox:focus-within,
    section[data-testid="stSidebar"] .stMultiSelect:focus-within,
    section[data-testid="stSidebar"] .stSlider:focus-within {
        border-left:4px solid #6366f1;
        padding-left:6px;
    }

    /* MULTISELECT TAGS */

    [data-baseweb="tag"] {
        background-color:#ede9fe !important;
        color:#5b21b6 !important;
    }

    </style>
    """, unsafe_allow_html=True)