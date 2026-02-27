# Architecture Overview

The Port Risk Monitor is organized as a modular pipeline that ingests raw AIS data,
transforms it into operational features, trains a machine learning model, and
presents results in an interactive dashboard. Below is a high‑level overview:

1. **Data Ingestion (src/ingest_ais.py)** – Reads raw AIS CSV files, validates
   required columns, converts timestamps to timezone‑aware pandas datetimes,
   casts numeric types, and writes a cleaned, sorted CSV. This step drops
   incomplete records and ensures data consistency.

2. **Feature Engineering (src/features.py)** – For each port defined in
   `data/sample/ports_us_sample.csv`, the AIS points within a geodesic radius are
   binned into time intervals (default 30 minutes). The script computes vessel
   counts, average and percentile speed statistics, anchored ratio (slow or
   stationary vessels), and derives a simple risk label based on upper quartile
   thresholds.

3. **Model Training (src/model.py)** – Consumes the cleaned AIS data and
   engineered features, trains a RandomForest classifier with balanced class
   weights, evaluates performance via AUC, serializes the model alongside the
   feature list using `joblib`, and writes the time‑series features for use in
   the dashboard.

4. **Dashboard (src/app.py)** – A Streamlit application that loads the time‑
   series features and trained model, allows users to select a port, visualizes
   vessel counts and anchored ratio over time, computes the risk score for
   recent observations, and triggers alerts when the risk exceeds a user‑set
   threshold. The dashboard runs locally but can be deployed to a cloud
   container platform for real‑time monitoring.

Future upgrades include integrating external data sources such as NOAA weather
and satellite imagery, adding anomaly detection for equipment downtime, and
providing APIs for automated alerting.
