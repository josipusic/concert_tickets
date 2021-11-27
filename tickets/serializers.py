from rest_framework import serializers

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    is_paid = serializers.SerializerMethodField()
    concert = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        exclude = 'customer',

    @staticmethod
    def get_is_paid(obj):
        return True if obj.amount_paid > 0 else False

    @staticmethod
    def get_concert(obj):
        return obj.concert.name
