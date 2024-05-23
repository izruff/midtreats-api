from django.db import models

class User(models.Model):
    """
    Represents a registered user.
    """

    username = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    preference = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
