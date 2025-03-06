from flask_migrate import Migrate
from app import create_app
from models import db
import click

app = create_app('dev')
migrate = Migrate(app, db)

@click.group()
def cli():
    """Command line interface for flask-migrate operations."""
    pass

@click.command()
def init():
    """Initialize migrations."""
    from flask_migrate import init as fm_init
    with app.app_context():
        fm_init()

@click.command()
@click.option('--message', '-m', default=None, help='Migration message')
def migrate(message):
    """Generate a new migration."""
    from flask_migrate import migrate as fm_migrate
    with app.app_context():
        fm_migrate(message=message)

@click.command()
def upgrade():
    """Apply all migrations."""
    from flask_migrate import upgrade as fm_upgrade
    with app.app_context():
        fm_upgrade()

cli.add_command(init)
cli.add_command(migrate)
cli.add_command(upgrade)

if __name__ == '__main__':
    cli()
