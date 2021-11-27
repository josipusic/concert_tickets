from django.db import models
from catalog.models import Concert
from django.conf import settings


class TicketManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('concert')


class Ticket(models.Model):
    objects = TicketManager()

    concert = models.ForeignKey(Concert, models.DO_NOTHING)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'Ticket for {self.concert}'
