from django.contrib.sessions.backends.db import SessionStore

session_store = SessionStore()
session = session_store.load()
