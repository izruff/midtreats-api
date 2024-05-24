from common.apis.maps import MapsClient
from django.contrib.sessions.backends.db import SessionStore

maps_client = MapsClient()

session_store = SessionStore()
session = session_store.load()
