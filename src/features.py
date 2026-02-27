import pandas as pd
from utils import within_radius_km


def build_port_timeseries(ais_df: pd.DataFrame, ports_df: pd.DataFrame, freq="30min") -> pd.DataFrame:
    """
    Creates a time series per port with congestion features.
    """
    rows = []
    ais_df = ais_df.copy()
    ais_df["tbin"] = ais_df["timestamp"].dt.floor(freq)

    for _, port in ports_df.iterrows():
        pname = port["port_name"]
        plat, plon = float(port["lat"]), float(port["lon"])
        radius = float(port["radius_km"])

        # Mark AIS points within port radius
        mask = ais_df.apply(
            lambda r: within_radius_km(r["lat"], r["lon"], plat, plon, radius),
            axis=1
        )
        local = ais_df.loc[mask].copy()
        if local.empty:
            continue

        # Feature: counts and speed stats
        g = local.groupby("tbin")
        ts = g.agg(
            vessels=("mmsi", "nunique"),
            points=("mmsi", "size"),
            mean_sog=("sog", "mean"),
            p10_sog=("sog", lambda x: x.quantile(0.10)),
        ).reset_index()

        # Feature: anchored ratio (proxy for queueing)
        local["anchored"] = local["sog"] <= 0.5
        anchored = local.groupby("tbin")["anchored"].mean().reset_index(name="anchored_ratio")

        ts = ts.merge(anchored, on="tbin", how="left")
        ts["port_name"] = pname

        # Simple risk label proxy: high vessels + high anchored ratio
        # (Replace later with real congestion ground truth)
        ts["risk_label"] = (
            (ts["vessels"] >= ts["vessels"].quantile(0.75))
            & (ts["anchored_ratio"] >= ts["anchored_ratio"].quantile(0.75))
        ).astype(int)

        rows.append(ts)

    out = pd.concat(rows, ignore_index=True)
    return out
