from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import Genre, Artist


class Customer(AbstractUser):
    liked_genres = models.ManyToManyField(Genre, blank=True)
    liked_artists = models.ManyToManyField(Artist, blank=True)
