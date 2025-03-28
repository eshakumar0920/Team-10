"""Add reward system tables

Revision ID: reward_system_migration
Revises: (use your current latest migration here)
Create Date: 2025-03-28

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'reward_system_migration'
down_revision = '4eae0691e5f9'  # Replace with your current latest migration ID
branch_labels = None
depends_on = None

def upgrade():
    # Create reward_types table
    op.create_table(
        'reward_types',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('image_url', sa.String(255), nullable=False),
        sa.Column('tier', sa.Integer(), default=1),
        sa.Column('category', sa.String(50)),
        sa.Column('theme', sa.String(50)),
        sa.Column('is_rare', sa.Boolean(), default=False)
    )
    
    # Create user_rewards table
    op.create_table(
        'user_rewards',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('reward_type_id', sa.Integer(), sa.ForeignKey('reward_types.id'), nullable=False),
        sa.Column('acquired_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('is_equipped', sa.Boolean(), default=False),
        sa.Column('loot_box_id', sa.Integer(), sa.ForeignKey('loot_boxes.id'), nullable=True)
    )
    
    # Create loot_box_drop_rates table
    op.create_table(
        'loot_box_drop_rates',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('level_min', sa.Integer(), nullable=False),
        sa.Column('level_max', sa.Integer(), nullable=False),
        sa.Column('tier_1_rate', sa.Float(), default=0),
        sa.Column('tier_2_rate', sa.Float(), default=0),
        sa.Column('tier_3_rate', sa.Float(), default=0),
        sa.Column('tier_4_rate', sa.Float(), default=0)
    )
    
    # Create reward_drop_rates table
    op.create_table(
        'reward_drop_rates',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('loot_box_tier', sa.Integer(), nullable=False),
        sa.Column('tier_1_rate', sa.Float(), default=0),
        sa.Column('tier_2_rate', sa.Float(), default=0),
        sa.Column('tier_3_rate', sa.Float(), default=0),
        sa.Column('tier_4_rate', sa.Float(), default=0)
    )
    
    # Add relationship column to loot_boxes
    # First check if the column already exists
    inspector = sa.inspect(op.get_bind())
    columns = [col['name'] for col in inspector.get_columns('loot_boxes')]
    if 'rewards' not in columns:
        # No need to add the column - it's a relationship without a direct column
        pass

def downgrade():
    # Drop tables in reverse order
    op.drop_table('reward_drop_rates')
    op.drop_table('loot_box_drop_rates')
    op.drop_table('user_rewards')
    op.drop_table('reward_types')