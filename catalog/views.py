import stripe
from django.conf import settings
from django.db.models import F, Sum
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .custom_filters import FlippedOrderingFilter
from .models import Genre, Artist, Concert
from .serializers import GenreSerializer, ArtistSerializer, ConcertSerializer
from .sw_schemas import artist_list_sw_schema, concert_list_sw_schema, concert_detail_sw_schema

stripe.api_key = settings.STRIPE_SECRET_KEY


class GenresListAPIView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get(self, request, *args, **kwargs):
        """ List all genres. """
        return super().get(request, *args, **kwargs)


class ArtistsListApiView(ListAPIView):
    queryset = Artist.objects.select_related('genre')
    serializer_class = ArtistSerializer
    filter_backends = (FlippedOrderingFilter,)
    ordering_fields = ('popularity',)

    @artist_list_sw_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ConcertListApiView(ListAPIView):
    serializer_class = ConcertSerializer
    filter_backends = (FlippedOrderingFilter, SearchFilter)
    ordering_fields = ('popularity',)
    search_fields = ('name', 'artist__name')

    def get_queryset(self):
        queryset = Concert.objects.prefetch_related('artist__genre').annotate(
            popularity=Sum('artist__popularity') + F('tickets_sold')
        )
        artist = self.request.query_params.get('artist')
        if artist is not None:
            queryset = queryset.filter(artist__slug=artist.lower())

        return queryset

    @concert_list_sw_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ConcertDetailApiView(RetrieveAPIView):
    queryset = Concert.objects.annotate(popularity=Sum('artist__popularity') + F('tickets_sold'))
    serializer_class = ConcertSerializer
    lookup_field = 'slug'

    @concert_detail_sw_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request, slug):
    """ View that creates a Stripe checkout session and redirects to Stripe checkout page. """

    concert = Concert.objects.get_or_none(slug=slug)

    if concert:
        query_string = '?session_id={CHECKOUT_SESSION_ID}'
        success_url = f"{request.build_absolute_uri(reverse('create-ticket'))}{query_string}"
        cancel_url = request.build_absolute_uri(reverse('concert-detail', args=[slug]))

        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'hrk',
                    'product_data': {
                        'name': f'{concert.name} Concert Ticket',
                    },
                    'unit_amount': int(concert.ticket_price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={'concert_slug': slug}
        )

        return Response({'checkout_url': session.url})

    return Response({f'Concert with slug {slug} does not exist.'})
