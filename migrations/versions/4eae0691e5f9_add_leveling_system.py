"""Add leveling system

Revision ID: 4eae0691e5f9
Revises: 5a4e41c6c5f0
Create Date: 2025-03-27 19:10:02.847106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4eae0691e5f9'
down_revision = '5a4e41c6c5f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('loot_box_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('tier', sa.Integer(), nullable=True),
    sa.Column('icon_url', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('semesters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('loot_boxes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('is_opened', sa.Boolean(), nullable=True),
    sa.Column('awarded_at', sa.DateTime(), nullable=True),
    sa.Column('opened_at', sa.DateTime(), nullable=True),
    sa.Column('awarded_for', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['type_id'], ['loot_box_types.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_interactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('other_user_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('interaction_date', sa.DateTime(), nullable=True),
    sa.Column('semester', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['other_user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'other_user_id', 'event_id', name='unique_interaction')
    )
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('semester', sa.String(length=20), nullable=True))

    with op.batch_alter_table('levels', schema=None) as batch_op:
        batch_op.add_column(sa.Column('level_xp', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('total_xp', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('tier', sa.Integer(), nullable=True))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_event_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('active_weeks_streak', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('current_semester', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('current_tier', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('current_tier')
        batch_op.drop_column('current_semester')
        batch_op.drop_column('active_weeks_streak')
        batch_op.drop_column('last_event_date')

    with op.batch_alter_table('levels', schema=None) as batch_op:
        batch_op.drop_column('tier')
        batch_op.drop_column('total_xp')
        batch_op.drop_column('level_xp')

    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.drop_column('semester')

    op.drop_table('user_interactions')
    op.drop_table('loot_boxes')
    op.drop_table('semesters')
    op.drop_table('loot_box_types')
    # ### end Alembic commands ###
