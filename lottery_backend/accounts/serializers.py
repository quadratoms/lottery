from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.models import Group
from wallet.models import Wallet # Import Wallet model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number']

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Add user to the 'Player' group
        player_group, created = Group.objects.get_or_create(name='Player')
        user.groups.add(player_group)

        # Create a wallet for the new user
        Wallet.objects.create(user=user)

        return user
