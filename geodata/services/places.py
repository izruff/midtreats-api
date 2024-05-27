"""
Services for handling places-related operations, using the Places API
and session data to allow personalized results.
"""

from ...common.apis.maps import (
    MAX_RESTRICTION_RADIUS,
    MAX_RESULT_COUNT,
)

from . import (
    maps_client,
    session_store,
    session,
)

INITIAL_DISTANCE_THRESHOLD = 1000.0
DEFAULT_RESULT_PER_PAGE = 20
DEFAULT_PLACE_FIELDS = tuple()

def _get_preference_score(
    place_id,
    distance_rank=None,
    popularity_rank=None,
):
    """
    Returns score matching given the place ID based on user
    preferences, which is later used for sorting a list of places.
    
    The score is normalized to a scale of -1 to 1. A positive score
    means the user prefers the place, while a negative score means
    the opposite.

    NOTE: currently we are using a very simple preference model
    where each key in the preferences dict is a place type and the
    value is a boolean. Suppose X is the place referred by the place
    ID, and there is a key which is also one of the types of X. If
    the corresponding value is True, it fixes the score to 1 (the
    function returns immediately). Otherwise if False then it fixes
    the score to -1. If no such keys are found, return 0.

    We might implement a caching solution if the score is not so fast
    to compute.
    """
    place = get_place_details(place_id, fields=['types'])
    for type_str in place['types']:
        v = session['user'].preferences.get(type_str, None)
        if v is not None:
            return 1 if v else -1
    return 0

def _get_relevant_fields_for_preference():
    """
    Returns a list of fields that are needed to calculate a place's
    preference score.

    NOTE: see the _assign_preference_scores function.
    """
    return ['types']

def get_place_details(place_id, fields=DEFAULT_PLACE_FIELDS):
    """
    Returns information corresponding to the fields list about a place
    given its ID.

    NOTE: currently this function calls the API directly; we will use
    a caching/temporary storage solution later.
    """
    return maps_client.place(place_id, fields)

def get_nearby_places_sorted(
    location,
    max_distance=INITIAL_DISTANCE_THRESHOLD,
    location_restriction=None
):
    """
    Returns a list of places near the given location, sorted by
    user preferences.
    
    The results are combined from two API responses: one is ranked
    by distance and the other by popularity. They are then filtered
    and sorted by preference score.

    Since the Places v2 API can only output at most 20 results per
    request, the function will likewise return a limited number of
    results. For more results, use the get_all_nearby_places function.

    NOTE: we are currently ignoring the location_restriction argument.
    """
    if max_distance > MAX_RESTRICTION_RADIUS:
        raise ValueError('The max_distance value is too large.')

    relevant_fields = _get_relevant_fields_for_preference()
    places_sorted_by_distance = maps_client.places_nearby_v2(
        location,
        max_distance,
        fields=relevant_fields,
        rank_preference='DISTANCE',
    )['places']
    places_sorted_by_popularity = maps_client.places_nearby_v2(
        location,
        max_distance,
        fields=relevant_fields,
        rank_preference='POPULARITY',
    )['places']

    place_ids = [p['place_id'] for p in places_sorted_by_distance]
    place_ids.extend(p['place_id'] for p in places_sorted_by_popularity)
    return sort_places_by_preference(place_ids)

def get_all_nearby_places_sorted(
    location,
    location_restriction=None,
    page=1,
    result_per_page=DEFAULT_RESULT_PER_PAGE,
):
    """
    Returns a paginated list of places near the given location and
    (mostly) sorted by user preferences.

    It works the same way as the get_nearby_places function, but
    uses the old API to obtain more results. As such, the API
    costs are significantly higher and it should be used sparingly.
    """
    pass

def get_places_in_area_sorted(
    location_restriction=None,
    page=1,
    result_per_page=DEFAULT_RESULT_PER_PAGE,
):
    """
    Returns a paginated list of places in the given area and
    (mostly) sorted by user preferences.

    The main distinction from get_all_nearby_places_sorted is that
    the distance to a particular center is no longer a factor in
    the ranking. This is useful for exploring places in a specific
    area, such as a city or a country.
    """
    pass

def sort_places_by_preference(place_ids, filter_by_preference=True):
    """
    Sorts (and optionally filters) a list of places by preference,
    then returns a dictionary mapping the sorted places to their
    respective scores.
    """
    sorted_places = sorted(place_ids, key=_get_preference_score)
    if filter_by_preference:
        return filter(lambda p: p >= 0, sorted_places)
    else:
        return sorted_places
