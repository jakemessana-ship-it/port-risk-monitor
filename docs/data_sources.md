# Data Sources

The Port Risk Monitor is built entirely on open data to ensure transparency and
reproducibility. The primary data sources used in the MVP are:

## Automatic Identification System (AIS) Data

AIS broadcasts provide vessel positions, speed over ground, heading, and other
attributes. For this project, we ingest a CSV export of AIS messages with
columns:

- `timestamp` – ISO8601 UTC timestamp of the message
- `mmsi` – Maritime Mobile Service Identity (vessel identifier)
- `lat`, `lon` – Latitude and longitude in decimal degrees
- `sog` – Speed over ground in knots

We rely on open AIS feeds (e.g., U.S. Coast Guard or academic archives) for
training and demonstration. The sample data included in `data/sample/ais_sample.csv`
is synthetic to enable quick experimentation.

## Port Reference Data

The file `data/sample/ports_us_sample.csv` contains the latitude, longitude,
and radius (in kilometers) for a handful of major U.S. ports. This allows the
feature generator to geofence AIS messages to specific ports. You can expand
this file with additional ports or adjust radius values to reflect local
conditions.

## Future Data Sources

To enhance predictive power and situational awareness, the following open data
sources are envisioned for future integration:

- **NOAA Weather** – Forecasts and storm tracks to anticipate weather‑driven
  disruptions.
- **Satellite‑derived Activity** – Remote sensing products to infer container
  yard occupancy or berth utilization.
- **Terminal & Throughput Metrics** – Publicly available data on cargo volumes,
  crane moves, or trucking flows to correlate with congestion.

These additional inputs will enable more robust models and richer alerting
capabilities.
