"""
Tests for models
"""
# Django's Decimal data type
from decimal import Decimal
# Django's base test class for database-related tests
from django.test import TestCase
# Retrieves the currently active user model
from django.contrib.auth import get_user_model
# Import the models from the core app
from core import models


class ModelTests(TestCase):
    """Tests for the custom user model"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""

        # Define test email and password
        email = 'test@example.com'
        password = 'testpass123'

        # Create a new user with the specified email and password
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        # Check that the user's email is set correctly
        self.assertEqual(user.email, email)

        # Check that the password is stored correctly (hashed internally)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""

        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@EXAMPLE.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@EXAMPLE.com', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is successful"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description'
        )

        self.assertEqual(str(recipe), recipe.title)
