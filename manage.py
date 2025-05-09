"""
Flask Database Migration Management Script

Purpose:
This script provides a command-line interface for managing database migrations in a Flask application.
It enables version-controlled database schema changes that can be tracked alongside code changes.

Why this file is necessary:
1. Provides automated database schema management without manual SQL
2. Enables version control of database structure changes
3. Allows consistent migrations across development, testing, and production environments
4. Facilitates team collaboration by synchronizing database changes
5. Creates a standardized interface for executing migration operations
6. Ensures all database operations run within the proper application context

Usage:
- Initialize migrations: python manage.py init
- Create a new migration: python manage.py migrate -m "description"
- Apply pending migrations: python manage.py upgrade
"""

# Import the Migrate class from flask_migrate to handle database migrations
from flask_migrate import Migrate
# Import the create_app factory function from app.py
from app import create_app
# Import the database instance from models.py
from models import db
# Import click for creating command line interfaces
import click

# Create a Flask application instance with 'dev' configuration
app = create_app('dev')
# Initialize the migration engine with the app and database instances
migrate = Migrate(app, db)

@click.group()
def cli():
    """Command line interface for flask-migrate operations."""
    # This creates a group of commands that can be run from the command line
    pass

@click.command()
def init():
    """Initialize migrations."""
    # Import the init function from flask_migrate
    from flask_migrate import init as fm_init
    # Create an application context to ensure the app is properly configured
    with app.app_context():
        # Initialize the migrations directory structure and configuration
        fm_init()

@click.command()
@click.option('--message', '-m', default=None, help='Migration message')
def migrate(message):
    """Generate a new migration."""
    # Import the migrate function from flask_migrate
    from flask_migrate import migrate as fm_migrate
    # Create an application context
    with app.app_context():
        # Generate a new migration script based on the changes detected in models
        # The message parameter allows adding a description to the migration
        fm_migrate(message=message)

@click.command()
def upgrade():
    """Apply all migrations."""
    # Import the upgrade function from flask_migrate
    from flask_migrate import upgrade as fm_upgrade
    # Create an application context
    with app.app_context():
        # Apply all unapplied migrations to the database
        fm_upgrade()

# Add the custom commands to the CLI group
cli.add_command(init)
cli.add_command(migrate)
cli.add_command(upgrade)

# If this file is run directly (not imported), execute the CLI
if __name__ == '__main__':
    cli()