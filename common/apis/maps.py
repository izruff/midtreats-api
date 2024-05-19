import googlemaps
from . import GOOGLE_MAPS_API_KEY as API_KEY

# Wrapper for Google Maps API client and other utilities
class MapsClient:
    client = googlemaps.Client(key=API_KEY)

    # Copy all methods from googlemaps.Client
    def __getattr__(self, name):
        return getattr(self.client, name)
