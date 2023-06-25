"""upgrade expenses_categories table

Revision ID: 1d41e8858be2
Revises: e7cde02f2de8
Create Date: 2023-06-19 22:08:37.334082

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = '1d41e8858be2'
down_revision = 'e7cde02f2de8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('expenses_categories',
                  sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False))
    op.add_column('expenses_categories',
                  sa.Column('category', sa.String(), nullable=False))
    op.add_column('expenses_categories',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')))


def downgrade():
    op.drop_column('expenses_categories', 'expenses_categories')
