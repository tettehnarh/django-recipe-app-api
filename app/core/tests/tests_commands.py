"""
Test custom Django management commands
"""

# Import 'patch' to mock dependencies during testing
from unittest.mock import patch

# Custom error from psycopg2 for PostgreSQL connection errors
from psycopg2 import OperationalError as Psycopg2Error

# Used to call management commands in tests
from django.core.management import call_command
# Django's database operational error
from django.db.utils import OperationalError
# A lightweight test case for simple unit tests
from django.test import SimpleTestCase


# Mock the 'check' method in 'wait_for_db' command
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database is ready"""
        # Simulate the database being available immediately
        patched_check.return_value = True

        # Run the 'wait_for_db' command
        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    # Mock time.sleep to avoid actual delays during testing
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        # Simulate the db's availability after a few retries
        patched_check.side_effect = [
            Psycopg2Error] * 2 + [OperationalError] * 3 + [True]

        # Run the 'wait_for_db' command
        call_command('wait_for_db')

        # Verify the check was called six times (2 + 3 retries + final success)
        self.assertEqual(patched_check.call_count, 6)

        # Ensure the check was eventually called with the default database
        patched_check.assert_called_with(databases=['default'])
