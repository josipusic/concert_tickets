from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tickets.models import Ticket
from tickets.serializers import TicketSerializer
from .serializers import CustomerSerializer


class CustomerDetailAPIView(RetrieveAPIView):
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_related_tickets(request):
    """ List all tickets purchased by customer that is making a request. """
    related_tickets = Ticket.objects.filter(customer_id=request.user.id)
    return Response(TicketSerializer(related_tickets, many=True).data)
