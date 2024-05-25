from . import GOOGLE_MAPS_API_KEY as API_KEY
from googlemaps import Client, exceptions

PLACES_V2_BASE_URL = 'https://places.googleapis.com'
ROUTES_BASE_URL = 'https://routes.googleapis.com'

MAX_RESTRICTION_RADIUS = 50000.0
MAX_RESULT_COUNT = 20

PLACES_V2_FIELDS_BASIC = {
    'accessibilityOptions',
    'addressComponents',
    'adrFormatAddress',
    'businessStatus',
    'displayName',
    'formattedAddress',
    'googleMapsUri',
    'iconBackgroundColor',
    'iconMaskBaseUri',
    'id',
    'location',
    'name',
    'photos',
    'plusCode',
    'primaryType',
    'primaryTypeDisplayName',
    'shortFormattedAddress',
    'subDestinations',
    'types',
    'utcOffsetMinutes',
    'viewport',
}

PLACES_V2_FIELDS_ADVANCED = {
    'currentOpeningHours',
    'currentSecondaryOpeningHours',
    'internationalPhoneNumber',
    'nationalPhoneNumber',
    'priceLevel',
    'rating',
    'regularOpeningHours',
    'regularSecondaryOpeningHours',
    'userRatingCount',
    'websiteUri',
}

PLACES_V2_FIELDS_PREFERRED = {
    'allowsDogs',
    'curbsidePickup',
    'delivery',
    'dineIn',
    'editorialSummary',
    'evChargeOptions',
    'fuelOptions',
    'goodForChildren',
    'goodForGroups',
    'goodForWatchingSports',
    'liveMusic',
    'menuForChildren',
    'parkingOptions',
    'paymentOptions',
    'outdoorSeating',
    'reservable',
    'restroom',
    'reviews',
    'servesBeer',
    'servesBreakfast',
    'servesBrunch',
    'servesCocktails',
    'servesCoffee',
    'servesDesserts',
    'servesDinner',
    'servesLunch',
    'servesVegetarianFood',
    'servesWine',
    'takeout',
}

def _extract_body(response):
    if response.status_code != 200:
        raise exceptions.HTTPError(response.status_code)

    body = response.json()
    return body

class MapsClient:
    """
    Wrapper for Google Maps API client and other utilities

    The `googlemaps` package is community-supported and lacks some
    of the newer endpoints offered by the Maps API. We have included
    some of them in this wrapper, which we use for our services.

    We might move these to a separate package in the future.
    """

    def __init__(self):
        self.client = Client(key=API_KEY)

    def __getattr__(self, name):
        """Copies the methods of the client object."""
        return getattr(self.client, name)
    
    def place(
        self,
        place_id,
        fields,
        language_code=None,
        region_code=None,
        session_token=None,
    ):
        params = {}
        headers = {
            'X-Goog-FieldMask': ','.join(fields),
        }
        
        if language_code:
            params['languageCode'] = language_code
        if region_code:
            params['regionCode'] = region_code
        if session_token:
            params['sessionToken'] = session_token

        return self.client._request(f'/v1/places/{place_id}', {},  # No GET params
                                    base_url=PLACES_V2_BASE_URL,
                                    extract_body=_extract_body,
                                    requests_kwargs={'headers': headers})

    def places_nearby_v2(
        self,
        location,
        radius,
        fields,
        included_types=None,
        excluded_types=None,
        included_primary_types=None,
        excluded_primary_types=None,
        language_code=None,
        max_result_count=None,
        rank_preference=None,
        region_code=None,
    ):
        params: dict[str, object] = {
            'locationRestriction': {
                'circle': {
                    'center': {
                        'latitude': location[0],
                        'longitude': location[1],
                    },
                    'radius': radius,
                },
            },
        }
        headers = {
            'X-Goog-FieldMask': ','.join(
                fields.map(lambda s: f'places.{s}')),
        }
        
        if included_types:
            params['includedTypes'] = included_types
        if excluded_types:
            params['excludedTypes'] = excluded_types
        if included_primary_types:
            params['includedPrimaryTypes'] = included_primary_types
        if excluded_primary_types:
            params['excludedPrimaryTypes'] = excluded_primary_types
        if language_code:
            params['languageCode'] = language_code
        if max_result_count:
            params['maxResultCount'] = max_result_count
        if rank_preference:
            params['rankPreference'] = rank_preference
        if region_code:
            params['regionCode'] = region_code

        return self.client._request('/v1/places:searchNearby', {},  # No GET params
                                    base_url=PLACES_V2_BASE_URL,
                                    extract_body=_extract_body,
                                    post_json=params,
                                    requests_kwargs={'headers': headers})
