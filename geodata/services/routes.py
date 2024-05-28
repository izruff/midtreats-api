class RoutesService():
    """
    A collection of services for handling routes-related operations,
    using the Routes API and session data for personalized results.
    """

    def __init__(self, maps_client, session):
        self.maps_client = maps_client
        self.session = session

    def get_places_near_route_sorted(
        self,
        route,
        additional_preferences=None,
        max_count=20,
    ):
        """
        Returns a list of places near the given route sorted by preferences.
        This is used to give suggestions for new locations to visit along
        the route. 
        """
        pass

    def get_best_planned_routes(
        self,
        places_ordered,
        places_unordered,
        additional_preferences=None,
        max_count=3,
    ):
        """
        Returns the best planned routes for the given places according to
        preferences. The ordered places must keep the same order in the
        planned route, with the first place becoming the start of the
        route, and the last place becoming the end.
        """
        pass

    def add_places_into_planned_route(
        self,
        places,
        planned_route,
        additional_preferences=None,
        max_count=3,
    ):
        """
        Returns a new route that closely resembles the given planned route
        but with additional places, while taking into account other
        factors such as additional time taken.
        """
        pass
