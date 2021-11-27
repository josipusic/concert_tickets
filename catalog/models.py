from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class GetOrNoneManager(models.Manager):
    """
        Adds get_or_none manager method.
        example usage: Artist.objects.get_or_none(slug=...
    """

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class Genre(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Artist(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    popularity = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return self.name


class Concert(models.Model):
    objects = GetOrNoneManager()
    artist = models.ManyToManyField(Artist)
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    starts_at = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=5, decimal_places=2)
    tickets_sold = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
