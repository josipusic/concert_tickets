from rest_framework import serializers

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    is_paid = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = '__all__'

    @staticmethod
    def get_is_paid(obj):
        return True if obj.amount_paid > 0 else False
