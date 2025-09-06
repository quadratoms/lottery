from rest_framework import serializers
from .models import GameConfig, OddsScheme

class OddsSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OddsScheme
        fields = '__all__'

class GameConfigSerializer(serializers.ModelSerializer):
    odds_scheme = OddsSchemeSerializer(read_only=True)

    class Meta:
        model = GameConfig
        fields = '__all__'
