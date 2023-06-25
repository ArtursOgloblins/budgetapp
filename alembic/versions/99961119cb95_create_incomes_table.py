"""create incomes table

Revision ID: 99961119cb95
Revises: 
Create Date: 2023-06-19 21:13:58.340169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99961119cb95'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('expenses_categories', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('category', sa.String(), nullable=False))


def downgrade():
    op.drop_table('expenses_categories')
    pass