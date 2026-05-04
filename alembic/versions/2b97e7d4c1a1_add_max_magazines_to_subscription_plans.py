"""add max_magazines column to subscription_plans

Revision ID: 2b97e7d4c1a1
Revises: 94500a42b961
Create Date: 2026-04-24 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b97e7d4c1a1'
down_revision: Union[str, None] = '94500a42b961'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'subscription_plans',
        sa.Column('max_magazines', sa.Integer(), nullable=False, server_default='0'),
    )
    op.alter_column('subscription_plans', 'max_magazines', server_default=None)


def downgrade() -> None:
    op.drop_column('subscription_plans', 'max_magazines')
