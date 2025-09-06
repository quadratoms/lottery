from rest_framework import serializers
from .models import Draw

class DrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draw
        fields = '__all__'
