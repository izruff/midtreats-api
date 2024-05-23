from common.apis.maps import (
    MapsClient,
    MAX_RESTRICTION_RADIUS,
    MAX_RESULT_COUNT,
)

INITIAL_DISTANCE_THRESHOLD = 1000.0
DEFAULT_RESULT_PER_PAGE = 20

class PlacesService:
    """
    A service class for handling places-related operations. Each
    session is assigned a new instance to allow personalized results.
    """

    maps_client = MapsClient()

    def __init__(self, session):
        self.session = session

    def _assign_preference_scores(
        self,
        places,
        distance_rank=None,
        popularity_rank=None,
    ):
        """
        Returns a list of scores matching given list of places based
        on user preference, used for sorting a list of places.
        
        The scores are normalized to a scale of -1 to 1. A positive
        score means the user prefers the place, while a negative score
        means the opposite.
        """
        pass

    def get_nearby_places_sorted(
        self,
        location,
        location_restriction=None,
        max_result_count=None,
    ):
        """
        Returns a list of places near the given location, sorted by
        user preference.
        
        The results are combined from two API responses: one is ranked
        by distance and the other by popularity. They are then filtered
        and sorted by preference score.

        Since the Places v2 API can only output at most 20 results per
        request, the function will likewise return a limited number of
        results. For more results, use the get_all_nearby_places function.
        """
        pass

    def get_all_nearby_places_sorted(
        self,
        location,
        location_restriction=None,
        page=1,
        result_per_page=DEFAULT_RESULT_PER_PAGE,
    ):
        """
        Returns a paginated list of places near the given location and
        (mostly) sorted by user preference.

        It works the same way as the get_nearby_places function, but
        uses the old API to obtain more results. As such, the API
        costs are significantly higher and it should be used sparingly.
        """
        pass

    def get_places_in_area_sorted(
        self,
        location_restriction=None,
        page=1,
        result_per_page=DEFAULT_RESULT_PER_PAGE,
    ):
        """
        Returns a paginated list of places in the given area and
        (mostly) sorted by user preference.

        The main distinction from get_all_nearby_places_sorted is that
        the distance to a particular center is no longer a factor in
        the ranking. This is useful for exploring places in a specific
        area, such as a city or a country.
        """
        pass

    def sort_places_by_preference(self, places, filter=True):
        """
        Sorts (and optionally filters) a list of places by preference.
        """
        pass

    def filter_places_by_preference(self, places):
        """
        Filters a list of places by preference.
        """
        pass