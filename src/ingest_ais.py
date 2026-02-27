import argparse
import pandas as pd


def main():
    ap = argparse.ArgumentParser(description="Clean and sort AIS CSV data.")
    ap.add_argument("--input", required=True, help="Path to input AIS CSV file.")
    ap.add_argument("--out", required=True, help="Path to output cleaned CSV file.")
    args = ap.parse_args()

    df = pd.read_csv(args.input)
    # Ensure required columns exist
    required = {"timestamp", "mmsi", "lat", "lon", "sog"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Parse timestamp and drop rows with invalid values
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    df = df.dropna(subset=["timestamp", "mmsi", "lat", "lon", "sog"]).copy()

    # Cast types
    df["mmsi"] = df["mmsi"].astype(str)
    df["lat"] = df["lat"].astype(float)
    df["lon"] = df["lon"].astype(float)
    df["sog"] = df["sog"].astype(float)

    # Sort by timestamp then vessel id for deterministic ordering
    df = df.sort_values(["timestamp", "mmsi"])
    df.to_csv(args.out, index=False)
    print(f"Saved cleaned AIS to {args.out} ({len(df):,} rows)")


if __name__ == "__main__":
    main()
