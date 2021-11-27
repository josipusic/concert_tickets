import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from catalog.models import Concert
from .models import Ticket

stripe.api_key = settings.STRIPE_SECRET_KEY
Customer = get_user_model()


@swagger_auto_schema(method='GET', auto_schema=None)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def create_ticket(request):
    """ View that is redirected to from strip if payment is successful. """

    session = stripe.checkout.Session.retrieve(request.query_params.get('session_id'))
    item, *_ = session.list_line_items(session.stripe_id, limit=1).data
    concert = Concert.objects.get(slug=session.metadata.get('concert_slug'))

    Ticket.objects.create(
        concert=concert,
        customer=request.user,
        amount_paid=item.amount_total / 100
    )
    concert.tickets_sold += 1
    concert.save()

    return Response({f'You have successfully purchased a concert ticket for concert "{concert.name}"'})
