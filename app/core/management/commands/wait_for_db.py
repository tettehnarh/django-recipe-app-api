"""
Django command to wait for database to be available
"""

import time  # Used to delay retry attempts
# PostgreSQL-specific operational error
from psycopg2 import OperationalError as Psycopg2OpError
# Base class for creating custom management commands
from django.core.management.base import BaseCommand
# Django’s operational error for database issues
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        """Entrypoint for command execution"""

        # Notify the user while db is unavailable
        self.stdout.write('Waiting for database...')

        # Set a flag to track the database's availability
        db_up = False

        # Loop until the database connection is successful
        while db_up is False:
            try:
                # Check the connection to the default database
                self.check(databases=['default'])

                # If no exceptions are raised, the database is available
                db_up = True

            # Catch exceptions if the database is still unavailable
            except (Psycopg2OpError, OperationalError):

                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        # Notify the user that the database is now available
        self.stdout.write(self.style.SUCCESS('Database available!'))
