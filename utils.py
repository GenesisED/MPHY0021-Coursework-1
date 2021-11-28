import math as m

def haversine_distance(lat1, lon1, lat2, lon2):
    """Return the distance in km between two points around the Earth.

    Latitude and longitude for each point are given in degrees.
    """
    R = 6371
    d = 2*R*m.asin(m.sqrt((m.sin((lat2-lat1)/2))**2+m.cos(lat1)*m.cos(lat2)*(m.sin((lon2-lon1)/2))**2))
    return d