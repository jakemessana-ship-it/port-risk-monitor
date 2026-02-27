# Port Risk Monitor — AI-Powered Congestion & Infrastructure Risk for U.S. Ports

**Problem:** U.S. supply chains are vulnerable to port congestion and infrastructure disruption. A single disruption (weather, labor slowdown, equipment outage, channel blockage) can create cascading impacts across food, medical supplies, manufacturing inputs, and defense logistics.

**This project builds an operational, predictive risk dashboard** using open data (AIS vessel tracking + weather + throughput proxies) to estimate congestion risk and generate forward‑looking alerts.

---

## What this repo does (MVP)

✅ Ingests AIS vessel tracking data (CSV)

✅ Computes operational congestion signals:

- Vessel queue length near port anchorages
- Average speed anomalies (slowdowns / drift)
- Arrival density / burst detection
- Anchored vs. underway ratio

✅ Trains a baseline model to predict a **Port Congestion Risk Score** (0–100)

✅ Serves a lightweight dashboard (Streamlit) with:

- Live‑ish risk score over time
- Vessel counts near port
- Alert flags when risk crosses thresholds

---

## Why it’s useful operationally

Instead of reacting to a backlog after it happens, operators can:

- Re‑route cargo earlier
- Adjust berth allocation priorities
- Stage labor/equipment resources
- Trigger contingency contracts

---

## Quickstart

### 1) Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 2) Run the pipeline on sample data

```bash
# Clean the AIS sample data
python src/ingest_ais.py --input data/sample/ais_sample.csv --out data/processed/ais_clean.csv

# Train the baseline model and build port time series features
python src/model.py --ais data/processed/ais_clean.csv --ports data/sample/ports_us_sample.csv --out models/model.pkl
```

### 3) Launch dashboard

```bash
streamlit run src/app.py
```

### Data format (AIS CSV)

The MVP expects at minimum:

- `timestamp` (ISO8601)
- `mmsi` (vessel id)
- `lat`, `lon` (latitude, longitude)
- `sog` (speed over ground, knots)

E# Port Risk Monitor — AI-Powered Congestion & Infrastructure Risk for U.S. Ports

**Problem:** U.S. supply chains are vulnerable to port congestion and infrastructure disruption. A single disruption (weather, labor slowdown, equipment outage, channel blockage) can create cascading impacts across food, medical supplies, manufacturing inputs, and defense logistics.

**This project builds an operational, predictive risk dashboard** using open data (AIS vessel tracking + weather + throughput proxies) to estimate congestion risk and generate forward‑looking alerts.

---

## What this repo does (MVP)

✅ Ingests AIS vessel tracking data (CSV)

✅ Computes operational congestion signals:

- Vessel queue length near port anchorages
- Average speed anomalies (slowdowns / drift)
- Arrival density / burst detection
- Anchored vs. underway ratio

✅ Trains a baseline model to predict a **Port Congestion Risk Score** (0–100)

✅ Serves a lightweight dashboard (Streamlit) with:

- Live‑ish risk score over time
- Vessel counts near port
- Alert flags when risk crosses thresholds

---

## Why it’s useful operationally

Instead of reacting to a backlog after it happens, operators can:

- Re‑route cargo earlier
- Adjust berth allocation priorities
- Stage labor/equipment resources
- Trigger contingency contracts

---

## Quickstart

### 1) Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 2) Run the pipeline on sample data

```bash
# Clean the AIS sample data
python src/ingest_ais.py --input data/sample/ais_sample.csv --out data/processed/ais_clean.csv

# Train the baseline model and build port time series features
python src/model.py --ais data/processed/ais_clean.csv --ports data/sample/ports_us_sample.csv --out models/model.pkl
```

### 3) Launch dashboard

```bash
streamlit run src/app.py
```

### Data format (AIS CSV)

The MVP expects at minimum:

- `timestamp` (ISO8601)
- `mmsi` (vessel id)
- `lat`, `lon` (latitude, longitude)
- `sog` (speed over ground, knots)

Example row:

```csv
timestamp,mmsi,lat,lon,sog
2026-02-26T15:04:00Z,367123456,33.736,-118.262,0.2
```

---

## Success metrics (how you evaluate impact)

- Predictive accuracy of congestion events (AUC / F1)
- False alert rate
- Lead time (how early the system warns before congestion)
- Proxy operational benefit: reduced wait time / dwell time estimates

---

## Roadmap (next upgrades)

- Add NOAA weather + storm track features
- Add satellite‑derived port activity signals (e.g., vessel density / container yard occupancy proxies)
- Add berth utilization estimation using geofenced terminals
- Add anomaly detection for crane downtime proxies via vessel movement patterns
- Deploy as an API + event alerting pipeline

---

## Disclaimer

This is an open‑source educational prototype (not an official port operations product).
xample row:

```csv
timestamp,mmsi,lat,lon,sog
2026-02-26T15:04:00Z,367123456,33.736,-118.262,0.2
```

---

## Success metrics (how you evaluate impact)

- Predictive accuracy of congestion events (AUC / F1)
- False alert rate
- Lead time (how early the system warns before congestion)
- Proxy operational benefit: reduced wait time / dwell time estimates

---

## Roadmap (next upgrades)

- Add NOAA weather + storm track features
- Add satellite‑derived port activity signals (e.g., vessel density / container yard occupancy proxies)
- Add berth utilization estimation using geofenced terminals
- Add anomaly detection for crane downtime proxies via vessel movement patterns
- Deploy as an API + event alerting pipeline

---

## Disclaimer

This is an open‑source educational prototype (not an official port operations product).
