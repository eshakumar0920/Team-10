"""Fix users id sequence

Revision ID: 5a4e41c6c5f0
Revises: 
Create Date: 2025-03-14 12:37:17.100059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a4e41c6c5f0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create sequence for users.id
    op.execute("CREATE SEQUENCE IF NOT EXISTS users_id_seq")
    # Set it as the default for the column
    op.execute("ALTER TABLE users ALTER COLUMN id SET DEFAULT nextval('users_id_seq')")
    # Update the sequence to start from the current max ID
    op.execute("SELECT setval('users_id_seq', COALESCE((SELECT MAX(id) FROM users), 1))")

def downgrade():
    op.execute("ALTER TABLE users ALTER COLUMN id DROP DEFAULT")
    op.execute("DROP SEQUENCE IF EXISTS users_id_seq")
