import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from utils import load_pipeline
from recommendation_engine import classify_risk, retention_strategy

# ============================================================
# Page Config
# ============================================================

st.set_page_config(
    page_title="AI Churn Prediction System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# Custom CSS
# ============================================================

st.markdown("""
<style>
    /* Main background */
    .main { background-color: #0f1117; }

    /* KPI card */
    .kpi-card {
        background: linear-gradient(135deg, #1e2130, #262b3d);
        border: 1px solid #2e3450;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .kpi-label {
        font-size: 13px;
        color: #8b92a5;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
    }
    .kpi-sub {
        font-size: 12px;
        color: #5a6070;
        margin-top: 4px;
    }

    /* Section header */
    .section-header {
        font-size: 18px;
        font-weight: 600;
        color: #c9d1e0;
        border-left: 4px solid #4f8ef7;
        padding-left: 12px;
        margin: 24px 0 16px 0;
    }

    /* History table */
    .history-row {
        background: #1a1e2e;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 6px;
        border: 1px solid #2a2f45;
        font-size: 13px;
        color: #c9d1e0;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #13161f;
        border-right: 1px solid #1e2235;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #4f8ef7, #7b5ea7);
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        padding: 12px;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.88; }

    /* Divider */
    .main hr { border-color: #2a2f45; position: static !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Load Pipeline
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
# Session State — Prediction History
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

# ============================================================
# Sample Customers
# ============================================================

SAMPLES = {
    "-- Select a sample --": None,
    "🟢 Low Risk Sample": {
        "gender": "Male",   "SeniorCitizen": "No",  "Partner": "Yes",
        "Dependents": "Yes", "tenure": 60,           "PhoneService": "Yes",
        "MultipleLines": "No",  "InternetService": "DSL",
        "OnlineSecurity": "Yes", "OnlineBackup": "Yes",
        "DeviceProtection": "Yes", "TechSupport": "Yes",
        "StreamingTV": "No",  "StreamingMovies": "No",
        "Contract": "Two year", "PaperlessBilling": "No",
        "PaymentMethod": "Bank transfer (automatic)",
        "MonthlyCharges": 45.0, "TotalCharges": 2700.0,
    },
    "🟡 Medium Risk Sample": {
        "gender": "Female", "SeniorCitizen": "No",  "Partner": "No",
        "Dependents": "No",  "tenure": 24,           "PhoneService": "Yes",
        "MultipleLines": "Yes", "InternetService": "Fiber optic",
        "OnlineSecurity": "No",  "OnlineBackup": "Yes",
        "DeviceProtection": "No", "TechSupport": "No",
        "StreamingTV": "Yes", "StreamingMovies": "Yes",
        "Contract": "One year", "PaperlessBilling": "Yes",
        "PaymentMethod": "Credit card (automatic)",
        "MonthlyCharges": 80.0, "TotalCharges": 1920.0,
    },
    "🔴 High Risk Sample": {
        "gender": "Male",   "SeniorCitizen": "Yes", "Partner": "No",
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
# Sidebar
# ============================================================

st.sidebar.markdown("## 📋 Customer Information")
sample_choice = st.sidebar.selectbox("⚡ Quick-fill sample", list(SAMPLES.keys()))
s = SAMPLES[sample_choice] or {}

def sb_select(label, options, key):
    idx = options.index(s[key]) if key in s and s[key] in options else 0
    return st.sidebar.selectbox(label, options, index=idx)

def sb_slider(label, lo, hi, key, default):
    return st.sidebar.slider(label, lo, hi, s.get(key, default))

def sb_number(label, lo, hi, key, default):
    return st.sidebar.number_input(label, float(lo), float(hi),
                                   float(s.get(key, default)), step=0.01)

st.sidebar.markdown("---")
st.sidebar.markdown("**👤 Demographics**")
gender     = sb_select("Gender",         ["Male", "Female"], "gender")
senior     = sb_select("Senior Citizen", ["No", "Yes"],      "SeniorCitizen")
partner    = sb_select("Partner",        ["No", "Yes"],      "Partner")
dependents = sb_select("Dependents",     ["No", "Yes"],      "Dependents")

st.sidebar.markdown("---")
st.sidebar.markdown("**🗂️ Account Details**")
tenure          = sb_slider("Tenure (months)", 0, 72, "tenure", 12)
contract        = sb_select("Contract",
                    ["Month-to-month", "One year", "Two year"], "Contract")
paperless       = sb_select("Paperless Billing", ["No", "Yes"], "PaperlessBilling")
payment         = sb_select("Payment Method",
                    ["Electronic check", "Mailed check",
                     "Bank transfer (automatic)", "Credit card (automatic)"],
                    "PaymentMethod")
monthly_charges = sb_number("Monthly Charges ($)", 0.0, 200.0,   "MonthlyCharges", 70.0)
total_charges   = sb_number("Total Charges ($)",   0.0, 10000.0, "TotalCharges",  1000.0)

st.sidebar.markdown("---")
st.sidebar.markdown("**📡 Services**")
phone_service  = sb_select("Phone Service",     ["No", "Yes"],                              "PhoneService")
multiple_lines = sb_select("Multiple Lines",    ["No phone service", "No", "Yes"],          "MultipleLines")
internet       = sb_select("Internet Service",  ["DSL", "Fiber optic", "No"],               "InternetService")
online_sec     = sb_select("Online Security",   ["No", "Yes", "No internet service"],       "OnlineSecurity")
online_bkp     = sb_select("Online Backup",     ["No", "Yes", "No internet service"],       "OnlineBackup")
device_prot    = sb_select("Device Protection", ["No", "Yes", "No internet service"],       "DeviceProtection")
tech_support   = sb_select("Tech Support",      ["No", "Yes", "No internet service"],       "TechSupport")
streaming_tv   = sb_select("Streaming TV",      ["No", "Yes", "No internet service"],       "StreamingTV")
streaming_mov  = sb_select("Streaming Movies",  ["No", "Yes", "No internet service"],       "StreamingMovies")

# ============================================================
# Input DataFrame
# ============================================================

input_data = pd.DataFrame([{
    "tenure"          : tenure,
    "MonthlyCharges"  : monthly_charges,
    "TotalCharges"    : total_charges,
    "gender"          : gender,
    "SeniorCitizen"   : senior,
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
}])

# ============================================================
# Helper — Plotly Charts
# ============================================================

def probability_gauge(probability):
    color = "#e74c3c" if probability >= 0.7 else "#f39c12" if probability >= 0.4 else "#2ecc71"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(probability * 100, 1),
        number={"suffix": "%", "font": {"size": 36, "color": "#ffffff"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#8b92a5",
                     "tickfont": {"color": "#8b92a5"}},
            "bar":  {"color": color, "thickness": 0.25},
            "bgcolor": "#1e2130",
            "bordercolor": "#2e3450",
            "steps": [
                {"range": [0,  40], "color": "#1a2e1a"},
                {"range": [40, 70], "color": "#2e2a14"},
                {"range": [70, 100],"color": "#2e1a1a"},
            ],
            "threshold": {
                "line": {"color": color, "width": 3},
                "thickness": 0.8,
                "value": probability * 100
            }
        },
        title={"text": "Churn Probability", "font": {"color": "#8b92a5", "size": 14}}
    ))
    fig.update_layout(
        height=260,
        margin=dict(t=40, b=10, l=20, r=20),
        paper_bgcolor="#1e2130",
        font_color="#ffffff"
    )
    return fig


def probability_bar(probability):
    stay  = round((1 - probability) * 100, 1)
    churn = round(probability * 100, 1)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Will Stay",  x=["Prediction"], y=[stay],
        marker_color="#2ecc71", text=[f"{stay}%"], textposition="inside",
        textfont={"color": "white", "size": 14}
    ))
    fig.add_trace(go.Bar(
        name="Will Churn", x=["Prediction"], y=[churn],
        marker_color="#e74c3c", text=[f"{churn}%"], textposition="inside",
        textfont={"color": "white", "size": 14}
    ))
    fig.update_layout(
        barmode="stack",
        height=260,
        margin=dict(t=30, b=10, l=10, r=10),
        paper_bgcolor="#1e2130",
        plot_bgcolor="#1e2130",
        font_color="#c9d1e0",
        legend=dict(bgcolor="#1e2130", font={"color": "#c9d1e0"}),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False, range=[0, 100], ticksuffix="%"),
        title=dict(text="Stay vs Churn Probability", font={"color": "#8b92a5", "size": 14})
    )
    return fig


def customer_metrics_chart(tenure_val, monthly_val, total_val):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Tenure (months)", "Monthly Charges ($)", "Total Charges ($)"],
        y=[tenure_val, monthly_val, total_val],
        marker_color=["#4f8ef7", "#7b5ea7", "#f39c12"],
        text=[str(tenure_val), f"${monthly_val:.0f}", f"${total_val:.0f}"],
        textposition="outside",
        textfont={"color": "#c9d1e0", "size": 12}
    ))
    fig.update_layout(
        height=280,
        margin=dict(t=30, b=10, l=10, r=10),
        paper_bgcolor="#1e2130",
        plot_bgcolor="#1e2130",
        font_color="#c9d1e0",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        title=dict(text="Customer Financial Profile", font={"color": "#8b92a5", "size": 14})
    )
    return fig

# ============================================================
# Main Page Header
# ============================================================

st.markdown("""
<div style='padding: 8px 0 4px 0;'>
    <h1 style='color:#ffffff; font-size:28px; font-weight:700; margin:0;'>
        📊 AI-Powered Customer Retention System
    </h1>
    <p style='color:#8b92a5; font-size:14px; margin:4px 0 0 0;'>
        IBM Telco Churn Prediction &nbsp;|&nbsp; ML Pipeline &nbsp;|&nbsp; Real-time Risk Analysis
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# Live KPI Cards (always visible, update after prediction)
# ============================================================

st.markdown("<div class='section-header'>📌 Customer Snapshot</div>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
k1.markdown(f"""
<div class='kpi-card'>
    <div class='kpi-label'>Tenure</div>
    <div class='kpi-value'>{tenure}</div>
    <div class='kpi-sub'>months</div>
</div>""", unsafe_allow_html=True)

k2.markdown(f"""
<div class='kpi-card'>
    <div class='kpi-label'>Monthly Charges</div>
    <div class='kpi-value'>${monthly_charges:.0f}</div>
    <div class='kpi-sub'>per month</div>
</div>""", unsafe_allow_html=True)

k3.markdown(f"""
<div class='kpi-card'>
    <div class='kpi-label'>Total Charges</div>
    <div class='kpi-value'>${total_charges:.0f}</div>
    <div class='kpi-sub'>lifetime value</div>
</div>""", unsafe_allow_html=True)

k4.markdown(f"""
<div class='kpi-card'>
    <div class='kpi-label'>Contract Type</div>
    <div class='kpi-value' style='font-size:18px;'>{contract}</div>
    <div class='kpi-sub'>{payment[:18]}...</div>
</div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# Predict Button
# ============================================================

predict_clicked = st.button("🔍 Predict Churn", use_container_width=True)

# ============================================================
# Prediction Results
# ============================================================

if predict_clicked:

    # --- Column validation ---
    expected = (
        pipeline.named_steps["preprocessor"].transformers[0][2] +
        pipeline.named_steps["preprocessor"].transformers[1][2]
    )
    missing = set(expected) - set(input_data.columns)
    if missing:
        st.error(f"❌ Missing columns: {missing}")
        st.stop()

    prediction  = pipeline.predict(input_data)[0]
    probability = pipeline.predict_proba(input_data)[0][1]
    risk        = classify_risk(probability)
    recommend   = retention_strategy(risk)

    # --- Save to history ---
    st.session_state.history.insert(0, {
        "Time"       : datetime.now().strftime("%H:%M:%S"),
        "Tenure"     : tenure,
        "Monthly $"  : f"${monthly_charges:.0f}",
        "Probability": f"{probability:.1%}",
        "Risk"       : risk,
        "Prediction" : "Churn" if prediction == 1 else "Stay",
    })

    st.markdown("---")

    # ============================================================
    # Section: Prediction Results
    # ============================================================

    st.markdown("<div class='section-header'>🎯 Prediction Results</div>", unsafe_allow_html=True)

    r1, r2, r3 = st.columns(3)
    r1.metric("Churn Probability", f"{probability:.2%}")
    r2.metric("Risk Level", risk)
    r3.metric("Prediction", "⚠️ Will Churn" if prediction == 1 else "✅ Will Stay")

    st.markdown("<br>", unsafe_allow_html=True)

    if prediction == 1:
        st.error("❌  This customer is likely to churn. Immediate action recommended.")
    else:
        st.success("✅  This customer is not likely to churn. Continue engagement strategy.")

    # ============================================================
    # Section: Risk Analysis
    # ============================================================

    st.markdown("<div class='section-header'>🔎 Risk Analysis</div>", unsafe_allow_html=True)

    if risk == "High Risk":
        st.error(f"🔴 Risk Level: **{risk}** — Customer has a high probability of leaving.")
    elif risk == "Medium Risk":
        st.warning(f"🟡 Risk Level: **{risk}** — Customer shows moderate churn signals.")
    else:
        st.success(f"🟢 Risk Level: **{risk}** — Customer appears stable and satisfied.")

    # ============================================================
    # Section: Analytics Dashboard
    # ============================================================

    st.markdown("<div class='section-header'>📈 Analytics Dashboard</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.plotly_chart(probability_gauge(probability),    use_container_width=True)
    with c2:
        st.plotly_chart(probability_bar(probability),      use_container_width=True)
    with c3:
        st.plotly_chart(
            customer_metrics_chart(tenure, monthly_charges, total_charges),
            use_container_width=True
        )

    # ============================================================
    # Section: Retention Recommendation
    # ============================================================

    st.markdown("<div class='section-header'>💡 Retention Recommendation</div>", unsafe_allow_html=True)

    rec_color = {"High Risk": "#e74c3c", "Medium Risk": "#f39c12", "Low Risk": "#2ecc71"}
    st.markdown(f"""
    <div style='background:#1e2130; border-left:4px solid {rec_color[risk]};
                border-radius:8px; padding:16px 20px; color:#c9d1e0; font-size:15px;'>
        <strong style='color:{rec_color[risk]};'>{risk}</strong> &nbsp;→&nbsp; {recommend}
    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    # Section: Customer Data
    # ============================================================

    st.markdown("<div class='section-header'>📋 Customer Information</div>", unsafe_allow_html=True)

    with st.expander("View full customer profile", expanded=False):
        display_df = input_data.T.rename(columns={0: "Value"})
        display_df.index.name = "Feature"
        st.dataframe(display_df, use_container_width=True)

# ============================================================
# Section: Prediction History
# ============================================================

if st.session_state.history:
    st.markdown("---")
    st.markdown("<div class='section-header'>🕘 Prediction History</div>", unsafe_allow_html=True)

    history_df = pd.DataFrame(st.session_state.history)

    def style_prediction(val):
        return "color: #e74c3c; font-weight:600;" if val == "Churn" else "color: #2ecc71; font-weight:600;"

    def style_risk(val):
        if val == "High Risk":   return "color: #e74c3c;"
        if val == "Medium Risk": return "color: #f39c12;"
        return "color: #2ecc71;"

    styled = (
        history_df.style
        .applymap(style_prediction, subset=["Prediction"])
        .applymap(style_risk,       subset=["Risk"])
    )

    st.dataframe(styled, use_container_width=True, hide_index=True)

    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()
