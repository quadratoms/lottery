from django.test import TestCase
from accounts.serializers import RegistrationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationSerializerTest(TestCase):
    def test_valid_registration(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepassword123'
        }
        serializer = RegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertTrue(user.check_password('securepassword123'))

    def test_invalid_registration_missing_fields(self):
        data = {
            'username': 'newuser',
            'password': 'securepassword123'
        } # Missing email
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_invalid_registration_duplicate_username(self):
        User.objects.create_user(username='existinguser', email='existing@example.com', password='password')
        data = {
            'username': 'existinguser',
            'email': 'another@example.com',
            'password': 'securepassword123'
        }
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_invalid_registration_duplicate_email(self):
        User.objects.create_user(username='user1', email='duplicate@example.com', password='password')
        data = {
            'username': 'user2',
            'email': 'duplicate@example.com',
            'password': 'securepassword123'
        }
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)