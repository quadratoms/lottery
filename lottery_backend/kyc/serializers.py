from rest_framework import serializers
from .models import KycCheck

class KycInitiateSerializer(serializers.Serializer):
    bvn_nin = serializers.CharField(max_length=11) # BVN is 11 digits, NIN is 11 digits

class KycCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = KycCheck
        fields = '__all__'
