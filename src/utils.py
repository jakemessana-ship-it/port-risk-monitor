from geopy.distance import geodesic


def within_radius_km(lat, lon, port_lat, port_lon, radius_km: float) -> bool:
    """Return True if the point (lat, lon) lies within radius_km of the port.

    Args:
        lat (float): Latitude of the AIS point.
        lon (float): Longitude of the AIS point.
        port_lat (float): Latitude of the port center.
        port_lon (float): Longitude of the port center.
        radius_km (float): Search radius in kilometers.

    Returns:
        bool: True if the distance between the point and port is less than or equal to radius_km.
    """
    return geodesic((lat, lon), (port_lat, port_lon)).km <= radius_km
