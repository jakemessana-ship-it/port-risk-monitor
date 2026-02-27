import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Port Risk Monitor", layout="wide")

st.title("Port Risk Monitor")
st.caption("Predictive congestion + infrastructure risk signals using AIS-derived operational features.")


@st.cache_data
def load_ts():
    return pd.read_csv("data/processed/port_timeseries.csv", parse_dates=["tbin"])


@st.cache_resource
def load_model():
    return joblib.load("models/model.pkl")


ts = load_ts()

ports = sorted(ts["port_name"].unique().tolist())
port = st.sidebar.selectbox("Port", ports)

sub = ts[ts["port_name"] == port].copy().sort_values("tbin")

st.subheader(f"{port} — Risk Over Time")

col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.line_chart(sub.set_index("tbin")[["vessels", "anchored_ratio"]])

with col2:
    st.metric("Latest vessels in radius", int(sub["vessels"].iloc[-1]))
    st.metric("Latest anchored ratio", float(sub["anchored_ratio"].iloc[-1]))

    # Risk score (0-100) using trained model probability
    try:
        payload = load_model()
        model = payload["model"]
        feats = payload["features"]
        p = model.predict_proba(sub[feats].fillna(0))[:, 1]
        sub["risk_score"] = (p * 100).round(1)
        latest = float(sub["risk_score"].iloc[-1])
        st.metric("Risk score (0-100)", latest)

        threshold = st.slider("Alert threshold", 0, 100, 70)
        if latest >= threshold:
            st.error(f"ALERT: Risk score {latest} ≥ {threshold} — congestion likelihood elevated.")
        else:
            st.success("No alert — risk below threshold.")
    except Exception as e:
        st.warning(f"Model not loaded yet. Train first. Details: {e}")

st.subheader("Latest rows")
st.dataframe(sub.tail(20), use_container_width=True)
