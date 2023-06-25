"""delete column

Revision ID: ed4c225aea73
Revises: 99961119cb95
Create Date: 2023-06-19 21:38:55.602392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed4c225aea73'
down_revision = '99961119cb95'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('expenses_categories', 'category')


def downgrade():
    op.add_column('expenses_categories', sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'),
                                                   ondelete='CASCADE', nullable=False))
