import argparse
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from features import build_port_timeseries


FEATURES = ["vessels", "mean_sog", "p10_sog", "anchored_ratio"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ais", required=True)
    ap.add_argument("--ports", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    ais = pd.read_csv(args.ais)
    ais["timestamp"] = pd.to_datetime(ais["timestamp"], utc=True)

    ports = pd.read_csv(args.ports)

    ts = build_port_timeseries(ais, ports)
    if ts.empty:
        raise RuntimeError("No port time series generated. Check your AIS coordinates and port radius.")

    X = ts[FEATURES].fillna(0)
    y = ts["risk_label"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    model = RandomForestClassifier(n_estimators=300, random_state=42, class_weight="balanced")
    model.fit(X_train, y_train)

    proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, proba)
    print(f"AUC: {auc:.3f}")

    payload = {
        "model": model,
        "features": FEATURES
    }
    joblib.dump(payload, args.out)
    print(f"Saved model to {args.out}")
    ts.to_csv("data/processed/port_timeseries.csv", index=False)
    print("Saved features to data/processed/port_timeseries.csv")


if __name__ == "__main__":
    main()
