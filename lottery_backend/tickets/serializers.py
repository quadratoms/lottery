from rest_framework import serializers
from .models import Ticket

class TicketCreateSerializer(serializers.Serializer):
    game_id = serializers.IntegerField() # Assuming game_id is an integer for now
    draw_id = serializers.IntegerField() # Assuming draw_id is an integer for now
    selection = serializers.IntegerField(min_value=1, max_value=99)
    stake = serializers.DecimalField(max_digits=12, decimal_places=2)

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
