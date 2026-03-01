import argparse
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.dummy import DummyClassifier
from pathlib import Path
from features import build_port_timeseries


FEATURES = ["vessels", "mean_sog", "p10_sog", "anchored_ratio"]


def main() -> None:
    """Train a congestion risk model and output serialized model payload.

    This script reads cleaned AIS data and port definitions, builds per‑port time
    series features, trains a RandomForestClassifier with class balancing, computes
    AUC on a hold‑out test set, and saves the model along with feature list. It also
    writes the generated time series to `data/processed/port_timeseries.csv` for
    dashboard use.
    """
    ap = argparse.ArgumentParser(description="Train port congestion risk model.")
    ap.add_argument("--ais", required=True, help="Path to cleaned AIS CSV.")
    ap.add_argument("--ports", required=True, help="Path to port definitions CSV.")
    ap.add_argument("--out", required=True, help="Path to output model pickle file.")
    args = ap.parse_args()

    # Load data
    ais = pd.read_csv(args.ais)
    ais["timestamp"] = pd.to_datetime(ais["timestamp"], utc=True)
    ports = pd.read_csv(args.ports)

    # Build time series features
    ts = build_port_timeseries(ais, ports)
    if ts.empty:
        raise RuntimeError("No port time series generated. Check your AIS coordinates and port radius.")

    # Prepare features and labels
    X = ts[FEATURES].fillna(0)
    y = ts["risk_label"].astype(int)

    # If there is only one class in the labels, use a dummy classifier to avoid errors
    if y.nunique() < 2:
        # Train a classifier that always predicts the single available class
        model = DummyClassifier(strategy="constant", constant=y.iloc[0])
        model.fit(X, y)
        auc = None
        print("Only one class present in labels. Using DummyClassifier.")
    else:
        # Split data into train/test sets, stratifying by the label
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42, stratify=y
        )
        # Train model with balanced class weights
        model = RandomForestClassifier(
            n_estimators=300, random_state=42, class_weight="balanced"
        )
        model.fit(X_train, y_train)
        # Evaluate model
        proba = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, proba)
        print(f"AUC: {auc:.3f}")

    # Persist model
    payload = {
        "model": model,
        "features": FEATURES,
    }
    # Create directory for output model if it doesn't exist
    out_model_path = Path(args.out)
    out_model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(payload, out_model_path)
    print(f"Saved model to {out_model_path}")

    # Ensure the processed directory exists
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)
    # Save computed features for dashboard
    (out_dir / "port_timeseries.csv").write_text(ts.to_csv(index=False))
    print("Saved features to data/processed/port_timeseries.csv")


if __name__ == "__main__":
    main()
