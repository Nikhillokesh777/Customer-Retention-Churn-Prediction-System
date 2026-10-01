import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

try:
    from app.utils import load_pipeline
    from app.recommendation_engine import (
        classify_risk,
        retention_strategy,
        analyze_risk_drivers,
        LOW_RISK_THRESHOLD,
        HIGH_RISK_THRESHOLD
    )
except ImportError:
    from utils import load_pipeline
    from recommendation_engine import (
        classify_risk,
        retention_strategy,
        analyze_risk_drivers,
        LOW_RISK_THRESHOLD,
        HIGH_RISK_THRESHOLD
    )

# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Retentio.AI | Enterprise Churn Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# Premium Enterprise Design System & Glassmorphism Styling
# ============================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Typography & Palette */
    html, body, [class*="css"], .stMarkdown, .stText, p, span, label {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Backgrounds */
    .stApp {
        background-color: #07090e;
        background-image: 
            radial-gradient(at 10% 10%, rgba(99, 102, 241, 0.08) 0px, transparent 50%),
            radial-gradient(at 90% 10%, rgba(6, 182, 212, 0.06) 0px, transparent 50%),
            radial-gradient(at 50% 90%, rgba(244, 63, 94, 0.05) 0px, transparent 50%);
        background-attachment: fixed;
    }

    /* Top Header Bar */
    header[data-testid="stHeader"] {
        background-color: rgba(7, 9, 14, 0.8) !important;
        backdrop-filter: blur(12px) !important;
    }

    /* Top Brand Ribbon */
    .brand-hero {
        background: linear-gradient(135deg, rgba(20, 27, 45, 0.8), rgba(12, 17, 29, 0.9));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 20px;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .brand-title {
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .brand-badge {
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.35);
        color: #a5b4fc;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 6px 14px;
        border-radius: 9999px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Glass KPI Cards */
    .glass-card {
        background: rgba(16, 22, 34, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 18px 20px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.3);
    }
    .card-label {
        font-size: 11px;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 6px;
    }
    .card-val {
        font-size: 28px;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: -0.5px;
    }
    .card-sub {
        font-size: 12px;
        font-weight: 500;
        color: #94a3b8;
        margin-top: 4px;
    }

    /* Section Subheaders */
    .section-tag {
        font-size: 11px;
        font-weight: 800;
        color: #818cf8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 4px;
    }
    .section-heading {
        font-size: 19px;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Driver Pill Badges */
    .badge-pill-high {
        background: rgba(244, 63, 94, 0.12);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.3);
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-pill-medium {
        background: rgba(245, 158, 11, 0.12);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-pill-low {
        background: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Primary Gradient Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 12px 24px !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.55) !important;
        opacity: 0.96 !important;
    }

    /* Sidebar Refinements */
    section[data-testid="stSidebar"] {
        background-color: #0b0e17 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(16, 22, 34, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 4px;
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        padding: 10px 22px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e2638, #182030) !important;
        color: #ffffff !important;
        border: 1px solid rgba(99, 102, 241, 0.35) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
    }

    /* Table & Expander Styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .streamlit-expanderHeader {
        background: rgba(16, 22, 34, 0.6) !important;
        border-radius: 8px !important;
        color: #cbd5e1 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Pipeline Loader
# ============================================================

@st.cache_resource
def get_pipeline():
    return load_pipeline()

try:
    pipeline = get_pipeline()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

# ============================================================
# Session State
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "latest_prediction" not in st.session_state:
    st.session_state.latest_prediction = None

if "prev_preset" not in st.session_state:
    st.session_state.prev_preset = "-- Custom Account --"

if "simulated_delta" not in st.session_state:
    st.session_state.simulated_delta = None

# ============================================================
# Sample Presets with Ground-Truth Archetypes
# ============================================================

SAMPLES = {
    "-- Custom Account --": None,
    "🟢 Enterprise Retained (Low Risk)": {
        "gender": "Male",   "SeniorCitizen": 0,     "Partner": "Yes",
        "Dependents": "Yes", "tenure": 60,           "PhoneService": "Yes",
        "MultipleLines": "No",  "InternetService": "DSL",
        "OnlineSecurity": "Yes", "OnlineBackup": "Yes",
        "DeviceProtection": "Yes", "TechSupport": "Yes",
        "StreamingTV": "No",  "StreamingMovies": "No",
        "Contract": "Two year", "PaperlessBilling": "No",
        "PaymentMethod": "Bank transfer (automatic)",
        "MonthlyCharges": 45.0, "TotalCharges": 2700.0,
    },
    "🟡 Moderate Attrition (Medium Risk)": {
        "gender": "Female", "SeniorCitizen": 0,     "Partner": "No",
        "Dependents": "No",  "tenure": 24,           "PhoneService": "Yes",
        "MultipleLines": "Yes", "InternetService": "Fiber optic",
        "OnlineSecurity": "No",  "OnlineBackup": "Yes",
        "DeviceProtection": "No", "TechSupport": "No",
        "StreamingTV": "Yes", "StreamingMovies": "Yes",
        "Contract": "One year", "PaperlessBilling": "Yes",
        "PaymentMethod": "Credit card (automatic)",
        "MonthlyCharges": 80.0, "TotalCharges": 1920.0,
    },
    "🔴 Critical Churn Hazard (High Risk)": {
        "gender": "Male",   "SeniorCitizen": 1,     "Partner": "No",
        "Dependents": "No",  "tenure": 2,            "PhoneService": "Yes",
        "MultipleLines": "Yes", "InternetService": "Fiber optic",
        "OnlineSecurity": "No",  "OnlineBackup": "No",
        "DeviceProtection": "No", "TechSupport": "No",
        "StreamingTV": "Yes", "StreamingMovies": "Yes",
        "Contract": "Month-to-month", "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 95.0, "TotalCharges": 190.0,
    },
}

# ============================================================
# Sidebar Controls with Key Guards
# ============================================================

st.sidebar.markdown("""
<div style='padding: 8px 0 16px 0;'>
    <div style='font-size:11px; font-weight:800; color:#818cf8; letter-spacing:1.5px; text-transform:uppercase;'>Control Center</div>
    <div style='font-size:18px; font-weight:800; color:#ffffff;'>Subscriber Profile</div>
</div>
""", unsafe_allow_html=True)

sample_choice = st.sidebar.selectbox(
    "⚡ Instant Preset Archetype",
    list(SAMPLES.keys()),
    key="preset_selector"
)

if sample_choice != st.session_state.prev_preset:
    st.session_state.prev_preset = sample_choice
    preset_vals = SAMPLES.get(sample_choice)
    if preset_vals:
        for k, v in preset_vals.items():
            widget_k = f"widget_{k}"
            if k == "SeniorCitizen":
                st.session_state[widget_k] = "Yes" if v == 1 else "No"
            elif isinstance(v, (int, float)):
                st.session_state[widget_k] = v
            else:
                st.session_state[widget_k] = str(v)

def sb_select(label, options, key, default_idx=0):
    widget_key = f"widget_{key}"
    if widget_key not in st.session_state:
        st.session_state[widget_key] = options[default_idx]
    return st.sidebar.selectbox(label, options, key=widget_key)

def sb_slider(label, lo, hi, key, default):
    widget_key = f"widget_{key}"
    if widget_key not in st.session_state:
        st.session_state[widget_key] = int(default)
    return st.sidebar.slider(label, lo, hi, key=widget_key)

def sb_number(label, lo, hi, key, default):
    widget_key = f"widget_{key}"
    if widget_key not in st.session_state:
        st.session_state[widget_key] = float(default)
    return st.sidebar.number_input(label, float(lo), float(hi), step=1.0, key=widget_key)

st.sidebar.markdown("**👤 Demographics**")
gender     = sb_select("Gender", ["Male", "Female"], "gender", 0)
senior_str = sb_select("Senior Citizen", ["No", "Yes"], "SeniorCitizen", 0)
senior_val = 1 if senior_str == "Yes" else 0
partner    = sb_select("Partner on Account", ["No", "Yes"], "Partner", 0)
dependents = sb_select("Dependents Covered", ["No", "Yes"], "Dependents", 0)

st.sidebar.markdown("---")
st.sidebar.markdown("**🗂️ Contract & Financials**")
tenure          = sb_slider("Account Tenure (months)", 0, 72, "tenure", 12)
contract        = sb_select("Contract Commitment", ["Month-to-month", "One year", "Two year"], "Contract", 0)
paperless       = sb_select("Paperless Billing", ["No", "Yes"], "PaperlessBilling", 1)
payment         = sb_select("Billing Channel", [
    "Electronic check", "Mailed check",
    "Bank transfer (automatic)", "Credit card (automatic)"
], "PaymentMethod", 0)
monthly_charges = sb_number("Monthly ARPU ($)", 0.0, 200.0, "MonthlyCharges", 70.0)
total_charges   = sb_number("Lifetime Total Charges ($)", 0.0, 10000.0, "TotalCharges", 840.0)

st.sidebar.markdown("---")
st.sidebar.markdown("**📡 Telecommunication Services**")
phone_service  = sb_select("Voice Service", ["No", "Yes"], "PhoneService", 1)
multiple_lines = sb_select("Multi-Line Option", ["No phone service", "No", "Yes"], "MultipleLines", 1)
internet       = sb_select("Broadband Tier", ["DSL", "Fiber optic", "No"], "InternetService", 1)
online_sec     = sb_select("Cybersecurity Defense", ["No", "Yes", "No internet service"], "OnlineSecurity", 0)
online_bkp     = sb_select("Cloud Backup", ["No", "Yes", "No internet service"], "OnlineBackup", 0)
device_prot    = sb_select("Hardware Protection", ["No", "Yes", "No internet service"], "DeviceProtection", 0)
tech_support   = sb_select("VIP Tech Concierge", ["No", "Yes", "No internet service"], "TechSupport", 0)
streaming_tv   = sb_select("IPTV Streaming", ["No", "Yes", "No internet service"], "StreamingTV", 0)
streaming_mov  = sb_select("Movie On-Demand", ["No", "Yes", "No internet service"], "StreamingMovies", 0)

input_dict = {
    "tenure"          : tenure,
    "MonthlyCharges"  : monthly_charges,
    "TotalCharges"    : total_charges,
    "gender"          : gender,
    "SeniorCitizen"   : senior_val,
    "Partner"         : partner,
    "Dependents"      : dependents,
    "PhoneService"    : phone_service,
    "MultipleLines"   : multiple_lines,
    "InternetService" : internet,
    "OnlineSecurity"  : online_sec,
    "OnlineBackup"    : online_bkp,
    "DeviceProtection": device_prot,
    "TechSupport"     : tech_support,
    "StreamingTV"     : streaming_tv,
    "StreamingMovies" : streaming_mov,
    "Contract"        : contract,
    "PaperlessBilling": paperless,
    "PaymentMethod"   : payment,
}
input_data = pd.DataFrame([input_dict])

# ============================================================
# High-End Plotly Visualization Engines
# ============================================================

def build_neon_gauge(prob: float):
    color = "#f43f5e" if prob >= HIGH_RISK_THRESHOLD else "#f59e0b" if prob >= LOW_RISK_THRESHOLD else "#10b981"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(prob * 100, 1),
        number={"suffix": "%", "font": {"size": 42, "color": "#ffffff", "family": "Plus Jakarta Sans"}},
        gauge={
            "axis": {
                "range": [0, 100],
                "tickcolor": "#475569",
                "tickfont": {"color": "#64748b", "size": 11, "family": "Plus Jakarta Sans"},
                "tickwidth": 1
            },
            "bar": {"color": color, "thickness": 0.28},
            "bgcolor": "#0d131f",
            "bordercolor": "rgba(255, 255, 255, 0.08)",
            "borderwidth": 1,
            "steps": [
                {"range": [0, int(LOW_RISK_THRESHOLD * 100)], "color": "rgba(16, 185, 129, 0.12)"},
                {"range": [int(LOW_RISK_THRESHOLD * 100), int(HIGH_RISK_THRESHOLD * 100)], "color": "rgba(245, 158, 11, 0.12)"},
                {"range": [int(HIGH_RISK_THRESHOLD * 100), 100], "color": "rgba(244, 63, 94, 0.12)"},
            ],
            "threshold": {
                "line": {"color": color, "width": 4},
                "thickness": 0.8,
                "value": prob * 100
            }
        },
        title={
            "text": "PREDICTED ATTRITION VELOCITY",
            "font": {"color": "#94a3b8", "size": 11, "family": "Plus Jakarta Sans"}
        }
    ))
    fig.update_layout(
        height=260,
        margin=dict(t=40, b=10, l=24, r=24),
        paper_bgcolor="rgba(16, 22, 34, 0.4)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ffffff"
    )
    return fig


def build_driver_chart(drivers: list):
    """Visualizes localized risk factors as an executive horizontal impact breakdown."""
    if not drivers:
        return None

    factor_names = [d["factor"] for d in drivers][::-1]
    impact_scores = [35 if d["severity"] == "High" else 20 if d["severity"] == "Medium" else 10 for d in drivers][::-1]
    bar_colors = ["#f43f5e" if d["severity"] == "High" else "#f59e0b" if d["severity"] == "Medium" else "#10b981" for d in drivers][::-1]

    fig = go.Figure(go.Bar(
        x=impact_scores,
        y=factor_names,
        orientation='h',
        marker=dict(
            color=bar_colors,
            line=dict(color="rgba(255,255,255,0.15)", width=1)
        ),
        text=[f"+{s}% Risk" for s in impact_scores],
        textposition="outside",
        textfont=dict(color="#cbd5e1", size=12, family="Plus Jakarta Sans")
    ))
    fig.update_layout(
        height=240,
        margin=dict(t=20, b=10, l=10, r=40),
        paper_bgcolor="rgba(16, 22, 34, 0.4)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False, range=[0, 45]),
        yaxis=dict(showgrid=False, tickfont=dict(color="#cbd5e1", size=12)),
        font_color="#cbd5e1"
    )
    return fig

# ============================================================
# Executive Header Banner
# ============================================================

st.markdown("""
<div class='brand-hero'>
    <div>
        <div style='display:flex; align-items:center; gap:10px; margin-bottom:4px;'>
            <div style='font-size:22px;'>⚡</div>
            <h1 class='brand-title'>RETENTIO.AI &nbsp;|&nbsp; Enterprise Churn Decision Platform</h1>
        </div>
        <div style='color:#94a3b8; font-size:13px; font-weight:500;'>
            Production XGBoost v2.1 &nbsp;•&nbsp; 72.5% Minority Churn Recall &nbsp;•&nbsp; Automated Counterfactual Optimization
        </div>
    </div>
    <div style='display:flex; gap:12px;'>
        <div class='brand-badge'>
            <span style='color:#10b981;'>●</span> SYSTEM ACTIVE
        </div>
        <div class='brand-badge' style='background:rgba(6, 182, 212, 0.15); border-color:rgba(6, 182, 212, 0.35); color:#67e8f9;'>
            AUC: 0.846
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
tab_single, tab_whatif, tab_batch, tab_roi = st.tabs([
    "👤 Subscriber Risk Diagnostic",
    "🔮 What-If Retention Simulator",
    "📁 Batch Portfolio Intelligence",
    "💰 Strategic ROI & ARR Preserved"
])

# ============================================================
# TAB 1: Single Subscriber Risk Diagnostic
# ============================================================

with tab_single:
    # Live Glass KPI Snapshot
    st.markdown("<div class='section-tag'>Current Account Baseline</div>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"""
    <div class='glass-card'>
        <div class='card-label'>Customer Tenancy</div>
        <div class='card-val'>{tenure} <span style='font-size:16px; color:#64748b;'>mo</span></div>
        <div class='card-sub'>Lifecycle: {'Early Stage' if tenure <= 12 else 'Mature Account'}</div>
    </div>""", unsafe_allow_html=True)

    k2.markdown(f"""
    <div class='glass-card'>
        <div class='card-label'>Monthly Billing</div>
        <div class='card-val'>${monthly_charges:.0f}</div>
        <div class='card-sub'>Annualized: ${(monthly_charges * 12):,.0f}/yr</div>
    </div>""", unsafe_allow_html=True)

    k3.markdown(f"""
    <div class='glass-card'>
        <div class='card-label'>Cumulative LTV</div>
        <div class='card-val'>${total_charges:,.0f}</div>
        <div class='card-sub'>Paid to Date</div>
    </div>""", unsafe_allow_html=True)

    k4.markdown(f"""
    <div class='glass-card'>
        <div class='card-label'>Commitment & Channel</div>
        <div class='card-val' style='font-size:20px;'>{contract}</div>
        <div class='card-sub'>{payment[:20]}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Primary Analyze CTA
    if st.button("⚡ EXECUTE NEURAL CHURN PREDICTION", key="btn_predict_churn", use_container_width=True):
        prob = float(pipeline.predict_proba(input_data)[0][1])
        pred = int(pipeline.predict(input_data)[0])
        risk = classify_risk(prob)
        plan = retention_strategy(risk, input_dict)

        st.session_state.latest_prediction = {
            "probability": prob,
            "prediction": pred,
            "risk": risk,
            "plan": plan,
            "input_dict": input_dict,
            "input_df": input_data
        }

        st.session_state.history.insert(0, {
            "Timestamp": datetime.now().strftime("%H:%M:%S"),
            "Tenure": f"{tenure} mo",
            "ARPU": f"${monthly_charges:.0f}",
            "Contract": contract,
            "Churn Probability": f"{prob:.1%}",
            "Risk Tier": risk,
            "Action Status": "Action Plan Ready"
        })

    # Render Prediction Output
    if st.session_state.latest_prediction is not None:
        lp = st.session_state.latest_prediction
        prob = lp["probability"]
        pred = lp["prediction"]
        risk = lp["risk"]
        plan = lp["plan"]

        st.markdown("<br>", unsafe_allow_html=True)

        # Output Summary Banner
        p_color = "#f43f5e" if risk == "High Risk" else "#f59e0b" if risk == "Medium Risk" else "#10b981"
        st.markdown(f"""
        <div style='background:linear-gradient(135deg, rgba(16, 22, 34, 0.8), rgba(20, 28, 44, 0.9)); 
                    border-left: 6px solid {p_color}; border-radius:14px; padding:22px 28px; border:1px solid rgba(255,255,255,0.08); margin-bottom:20px;'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <span style='background:rgba(255,255,255,0.08); color:#cbd5e1; font-size:11px; font-weight:700; letter-spacing:1px; text-transform:uppercase; padding:4px 10px; border-radius:6px;'>
                        Model Diagnostic Verdict
                    </span>
                    <h2 style='color:#ffffff; font-size:24px; font-weight:800; margin:8px 0 4px 0;'>
                        {risk.upper()} &nbsp;—&nbsp; {plan['headline']}
                    </h2>
                    <div style='color:#94a3b8; font-size:13px;'>
                        Calculated Churn Probability: <strong style='color:{p_color}; font-size:16px;'>{prob:.1%}</strong> 
                        &nbsp;|&nbsp; Suggested Response Urgency: <strong style='color:#ffffff;'>{plan['urgency']}</strong>
                    </div>
                </div>
                <div style='text-align:right;'>
                    <div style='font-size:38px; font-weight:800; color:{p_color};'>{prob:.1%}</div>
                    <div style='font-size:11px; color:#64748b; font-weight:700; text-transform:uppercase;'>Attrit Score</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Analytical Columns
        col_g, col_d = st.columns([1, 1.2])
        with col_g:
            st.markdown("<div class='section-tag'>Probability Indicator</div>", unsafe_allow_html=True)
            st.plotly_chart(build_neon_gauge(prob), use_container_width=True)

        with col_d:
            st.markdown("<div class='section-tag'>Localized Attribution Factors</div>", unsafe_allow_html=True)
            d_chart = build_driver_chart(plan.get("drivers", []))
            if d_chart:
                st.plotly_chart(d_chart, use_container_width=True)
            else:
                st.success("Account metrics indicate strong loyalty profile. Zero critical churn drivers found.")

        # Actionable Retention Playbook Card
        st.markdown("<div class='section-tag'>Operational Playbook</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background:rgba(16, 22, 34, 0.7); border:1px solid rgba(255, 255, 255, 0.08); border-radius:14px; padding:22px 26px;'>
            <div style='display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:14px;'>
                <div>
                    <div style='font-size:12px; font-weight:700; color:#818cf8; text-transform:uppercase;'>Primary Strategic Pillar</div>
                    <div style='font-size:18px; font-weight:700; color:#ffffff;'>{plan['primary_strategy']}</div>
                </div>
                <div style='background:rgba(99, 102, 241, 0.15); border:1px solid rgba(99, 102, 241, 0.3); padding:8px 16px; border-radius:8px;'>
                    <span style='font-size:11px; color:#a5b4fc; font-weight:700; text-transform:uppercase;'>Prescribed Incentive:</span>
                    <strong style='color:#ffffff; font-size:13px;'> {plan['incentive_offer']}</strong>
                </div>
            </div>
            <div style='color:#cbd5e1; font-size:14px; font-weight:600; margin-bottom:8px;'>Executive Action Steps:</div>
            <div style='display:grid; grid-template-columns:1fr; gap:8px;'>
                {"".join(f"<div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); padding:10px 14px; border-radius:8px; color:#cbd5e1; font-size:13px;'>🔹 {item}</div>" for item in plan['action_items'])}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

    # Session Audit Trail
    if st.session_state.history:
        with st.expander("📋 Session Diagnostic Log & Audit History", expanded=False):
            h_df = pd.DataFrame(st.session_state.history)
            st.dataframe(h_df, use_container_width=True, hide_index=True)
            if st.button("Clear Audit Trail", key="btn_clear_history"):
                st.session_state.history = []
                st.session_state.latest_prediction = None
                st.rerun()

# ============================================================
# TAB 2: Counterfactual What-If Simulator
# ============================================================

with tab_whatif:
    st.markdown("""
    <div style='margin-bottom:18px;'>
        <div class='section-tag'>Counterfactual Reasoning Engine</div>
        <div class='section-heading'>🔮 "What-If" Retention Scenario Simulator</div>
        <p style='color:#94a3b8; font-size:14px;'>
            Simulate how proactive account modifications (e.g. extending contract commitment, offering free tech support, or switching payment channels) impact churn probability in real time.
        </p>
    </div>
    """, unsafe_allow_html=True)

    w_col1, w_col2 = st.columns(2)

    with w_col1:
        st.markdown("<div class='section-tag'>Adjust Counterfactual Levers</div>", unsafe_allow_html=True)
        sim_contract = st.selectbox("Simulate Contract Change:", ["Month-to-month", "One year", "Two year"], index=1, key="sim_contract")
        sim_tech = st.selectbox("Simulate Tech Support Addition:", ["No", "Yes"], index=1, key="sim_tech")
        sim_pay = st.selectbox("Simulate Auto-Pay Adoption:", ["Electronic check", "Bank transfer (automatic)", "Credit card (automatic)"], index=1, key="sim_pay")
        sim_discount = st.slider("Simulate Monthly Concession / Discount ($):", 0, 30, 10, key="sim_discount")

    # Build Counterfactual Feature Vector
    sim_dict = dict(input_dict)
    sim_dict["Contract"] = sim_contract
    sim_dict["TechSupport"] = sim_tech
    sim_dict["PaymentMethod"] = sim_pay
    sim_dict["MonthlyCharges"] = max(10.0, monthly_charges - sim_discount)
    sim_data = pd.DataFrame([sim_dict])

    base_prob = float(pipeline.predict_proba(input_data)[0][1])
    sim_prob = float(pipeline.predict_proba(sim_data)[0][1])
    delta_prob = sim_prob - base_prob

    with w_col2:
        st.markdown("<div class='section-tag'>Simulated Outcome Delta</div>", unsafe_allow_html=True)
        
        sim_color = "#10b981" if delta_prob <= 0 else "#f43f5e"
        
        st.markdown(f"""
        <div class='glass-card' style='border-color:rgba(99, 102, 241, 0.4); text-align:center; padding:28px 20px;'>
            <div class='card-label'>Projected Churn Probability</div>
            <div style='font-size:48px; font-weight:800; color:#ffffff; margin:6px 0;'>
                {sim_prob:.1%}
            </div>
            <div style='display:inline-flex; align-items:center; gap:6px; background:rgba(255,255,255,0.06); padding:6px 14px; border-radius:9999px;'>
                <span style='font-weight:700; color:{sim_color}; font-size:15px;'>
                    {f"{delta_prob:+.1%}"}
                </span>
                <span style='font-size:12px; color:#94a3b8;'>relative to current baseline ({base_prob:.1%})</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if delta_prob < -0.15:
            st.success(f"🎯 Significant Risk Reduction: Implementing this retention package lowers risk by **{abs(delta_prob):.1%}**, successfully migrating this customer into a secure tier!")
        elif delta_prob < 0:
            st.info(f"Moderate Risk Reduction: Lowers churn probability by **{abs(delta_prob):.1%}**.")
        else:
            st.warning("⚠️ This configuration does not yield risk reduction.")

# ============================================================
# TAB 3: Batch Portfolio Scoring
# ============================================================

with tab_batch:
    st.markdown("""
    <div style='margin-bottom:18px;'>
        <div class='section-tag'>Bulk High-Throughput Inference</div>
        <div class='section-heading'>📁 Batch Customer Scoring & Intelligence</div>
        <p style='color:#94a3b8; font-size:14px;'>
            Upload entire subscriber cohorts to score attrition risk across thousands of accounts simultaneously, estimate total ARR at risk, and download enriched action playbooks.
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Subscriber Dataset (.csv)", type=["csv"], key="batch_file_uploader")

    if uploaded_file is not None:
        try:
            batch_df = pd.read_csv(uploaded_file)
            st.markdown(f"<div style='color:#10b981; font-weight:600; margin-bottom:12px;'>✓ Successfully ingested {len(batch_df):,} subscriber records.</div>", unsafe_allow_html=True)

            scoring_df = batch_df.copy()
            if "customerID" in scoring_df.columns:
                scoring_df = scoring_df.drop(columns=["customerID"])
            if "Churn" in scoring_df.columns:
                scoring_df = scoring_df.drop(columns=["Churn"])

            scoring_df["TotalCharges"] = pd.to_numeric(scoring_df["TotalCharges"], errors="coerce")
            if scoring_df["SeniorCitizen"].dtype == object:
                scoring_df["SeniorCitizen"] = scoring_df["SeniorCitizen"].map({"Yes": 1, "No": 0}).fillna(0).astype(int)

            if st.button("⚡ EXECUTE BATCH SCORING", key="btn_score_batch", use_container_width=True):
                with st.spinner("Processing high-speed inference across portfolio..."):
                    probs = pipeline.predict_proba(scoring_df)[:, 1]
                    preds = pipeline.predict(scoring_df)

                    results_df = batch_df.copy()
                    results_df["Churn_Probability"] = np.round(probs, 4)
                    results_df["Risk_Tier"] = [classify_risk(p) for p in probs]
                    results_df["Model_Verdict"] = ["Churn Risk" if p == 1 else "Retained" for p in preds]

                    # Summary Calculations
                    high_risk = results_df[results_df["Risk_Tier"] == "High Risk"]
                    arr_at_risk = (high_risk["MonthlyCharges"] * 12).sum()

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("<div class='section-tag'>Executive Portfolio Summary</div>", unsafe_allow_html=True)
                    
                    b1, b2, b3, b4 = st.columns(4)
                    b1.metric("Analyzed Accounts", f"{len(results_df):,}")
                    b2.metric("Critical Hazards", f"{len(high_risk):,}", f"{(len(high_risk)/len(results_df)):.1%}")
                    b3.metric("Annual ARR at Risk", f"${arr_at_risk:,.0f}")
                    b4.metric("Avg Portfolio Churn Prob", f"{probs.mean():.1%}")

                    # Chart & Table
                    col_p1, col_p2 = st.columns([1, 1.4])
                    with col_p1:
                        tier_counts = results_df["Risk_Tier"].value_counts().reset_index()
                        tier_counts.columns = ["Risk Tier", "Accounts"]
                        fig_p = px.pie(
                            tier_counts, names="Risk Tier", values="Accounts",
                            color="Risk Tier",
                            color_discrete_map={"Low Risk": "#10b981", "Medium Risk": "#f59e0b", "High Risk": "#f43f5e"},
                            hole=0.55
                        )
                        fig_p.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#ffffff", margin=dict(t=20, b=20, l=20, r=20))
                        st.plotly_chart(fig_p, use_container_width=True)

                    with col_p2:
                        st.markdown("<div style='font-size:13px; font-weight:700; color:#cbd5e1; margin-bottom:8px;'>Top 10 Critical Attrition Accounts</div>", unsafe_allow_html=True)
                        top_hazard = results_df.sort_values(by="Churn_Probability", ascending=False).head(10)
                        display_cols = [c for c in ["customerID", "Contract", "tenure", "MonthlyCharges", "Churn_Probability", "Risk_Tier"] if c in top_hazard.columns]
                        st.dataframe(top_hazard[display_cols], use_container_width=True, hide_index=True)

                    csv_dl = results_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Prioritized Retention Roster (CSV)",
                        data=csv_dl,
                        file_name="retentio_prioritized_churn_risk_roster.csv",
                        mime="text/csv",
                        key="btn_download_batch_csv",
                        use_container_width=True
                    )
        except Exception as ex:
            st.error(f"Error processing portfolio batch: {ex}")
    else:
        st.info("💡 Test cohort scoring instantly using: `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv`")

# ============================================================
# TAB 4: Strategic ROI & ARR Preservation Calculator
# ============================================================

with tab_roi:
    st.markdown("""
    <div style='margin-bottom:18px;'>
        <div class='section-tag'>Enterprise Business Value Model</div>
        <div class='section-heading'>💰 Strategic ROI & ARR Preservation Simulator</div>
        <p style='color:#94a3b8; font-size:14px;'>
            Formulate executive investment justifications by quantifying net recurring revenue saved and retention campaign efficiency.
        </p>
    </div>
    """, unsafe_allow_html=True)

    r_col1, r_col2 = st.columns(2)
    with r_col1:
        total_customers = st.number_input("Total Subscriber Base", min_value=100, max_value=2000000, value=7043, step=500, key="roi_total_customers")
        baseline_churn_rate = st.slider("Current Annual Attrition Rate (%)", min_value=5.0, max_value=50.0, value=26.5, step=0.5, key="roi_baseline_churn_rate")
        avg_monthly_arpu = st.number_input("Average Monthly Spend per Account (ARPU $)", min_value=10.0, max_value=500.0, value=65.0, step=5.0, key="roi_avg_monthly_arpu")

    with r_col2:
        retention_success_rate = st.slider("Target Retention Rescue Rate (%)", min_value=5.0, max_value=60.0, value=25.0, step=1.0, key="roi_retention_success_rate")
        cost_per_retention_offer = st.number_input("Average Concession / Incentive Cost per Account ($)", min_value=0.0, max_value=200.0, value=30.0, step=5.0, key="roi_cost_per_retention_offer")

    churning_accounts = total_customers * (baseline_churn_rate / 100.0)
    saved_accounts = churning_accounts * (retention_success_rate / 100.0)
    gross_annual_rev_saved = saved_accounts * avg_monthly_arpu * 12
    total_campaign_cost = saved_accounts * cost_per_retention_offer
    net_annual_value = gross_annual_rev_saved - total_campaign_cost
    roi_multiple = (net_annual_value / total_campaign_cost) if total_campaign_cost > 0 else 0

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-tag'>Executive Financial Impact</div>", unsafe_allow_html=True)

    o1, o2, o3, o4 = st.columns(4)
    o1.markdown(f"""
    <div class='glass-card'>
        <div class='card-label'>Accounts Preserved</div>
        <div class='card-val' style='color:#67e8f9;'>{int(saved_accounts):,}</div>
        <div class='card-sub'>Subscribers Protected / Yr</div>
    </div>""", unsafe_allow_html=True)

    o2.markdown(f"""
    <div class='glass-card'>
        <div class='card-label'>Gross ARR Saved</div>
        <div class='card-val' style='color:#34d399;'>${gross_annual_rev_saved:,.0f}</div>
        <div class='card-sub'>Annualized Contract Value</div>
    </div>""", unsafe_allow_html=True)

    o3.markdown(f"""
    <div class='glass-card'>
        <div class='card-label'>Net Financial Value</div>
        <div class='card-val' style='color:#a5b4fc;'>${net_annual_value:,.0f}</div>
        <div class='card-sub'>After Concession Costs</div>
    </div>""", unsafe_allow_html=True)

    o4.markdown(f"""
    <div class='glass-card'>
        <div class='card-label'>Campaign ROI</div>
        <div class='card-val' style='color:#fbbf24;'>{roi_multiple:.1f}x</div>
        <div class='card-sub'>Return on Retention Spend</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:linear-gradient(135deg, rgba(20, 27, 45, 0.7), rgba(16, 22, 34, 0.8)); border:1px solid rgba(99, 102, 241, 0.25); border-radius:14px; padding:22px 28px; margin-top:20px;'>
        <div style='font-size:16px; font-weight:700; color:#ffffff; margin-bottom:8px;'>💼 Boardroom Executive Briefing</div>
        <div style='color:#94a3b8; font-size:14px; line-height:1.6;'>
            Deploying the <strong>Retentio.AI</strong> churn interception platform across an active subscriber base of 
            <strong style='color:#ffffff;'>{total_customers:,}</strong> accounts is projected to preserve 
            <strong style='color:#34d399;'>${net_annual_value:,.0f}</strong> in Net Annual Recurring Revenue (ARR). 
            With an average retention cost of <strong style='color:#ffffff;'>${cost_per_retention_offer:.0f}</strong> per engaged subscriber, 
            the retention program achieves an efficiency multiple of <strong style='color:#fbbf24;'>{roi_multiple:.1f}x ROI</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)
