from apis import GOOGLE_MAPS_API_KEY as API_KEY
from googlemaps import Client, exceptions

PLACES_V2_BASE_URL = 'https://places.googleapis.com'
ROUTES_BASE_URL = 'https://routes.googleapis.com'

MAX_RESTRICTION_RADIUS = 50000.0
MAX_RESULT_COUNT = 20

PLACES_V2_FIELDS_BASIC = {
    'places.accessibilityOptions',
    'places.addressComponents',
    'places.adrFormatAddress',
    'places.businessStatus',
    'places.displayName',
    'places.formattedAddress',
    'places.googleMapsUri',
    'places.iconBackgroundColor',
    'places.iconMaskBaseUri',
    'places.id',
    'places.location',
    'places.name',
    'places.photos',
    'places.plusCode',
    'places.primaryType',
    'places.primaryTypeDisplayName',
    'places.shortFormattedAddress',
    'places.subDestinations',
    'places.types',
    'places.utcOffsetMinutes',
    'places.viewport',
}

PLACES_V2_FIELDS_ADVANCED = {
    'places.currentOpeningHours',
    'places.currentSecondaryOpeningHours',
    'places.internationalPhoneNumber',
    'places.nationalPhoneNumber',
    'places.priceLevel',
    'places.rating',
    'places.regularOpeningHours',
    'places.regularSecondaryOpeningHours',
    'places.userRatingCount',
    'places.websiteUri',
}

PLACES_V2_FIELDS_PREFERRED = {
    'places.allowsDogs',
    'places.curbsidePickup',
    'places.delivery',
    'places.dineIn',
    'places.editorialSummary',
    'places.evChargeOptions',
    'places.fuelOptions',
    'places.goodForChildren',
    'places.goodForGroups',
    'places.goodForWatchingSports',
    'places.liveMusic',
    'places.menuForChildren',
    'places.parkingOptions',
    'places.paymentOptions',
    'places.outdoorSeating',
    'places.reservable',
    'places.restroom',
    'places.reviews',
    'places.servesBeer',
    'places.servesBreakfast',
    'places.servesBrunch',
    'places.servesCocktails',
    'places.servesCoffee',
    'places.servesDesserts',
    'places.servesDinner',
    'places.servesLunch',
    'places.servesVegetarianFood',
    'places.servesWine',
    'places.takeout',
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
            'X-Goog-FieldMask': ','.join(fields),
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
