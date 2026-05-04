"""add status to rentals

Revision ID: 5dbf8d7780e1
Revises: 2b97e7d4c1a1
Create Date: 2026-04-24 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '5dbf8d7780e1'
down_revision: Union[str, None] = '74666597e362'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'rentals',
        sa.Column('status', sa.String(length=20), nullable=False, server_default='borrowed'),
    )
    op.alter_column('rentals', 'status', server_default=None)


def downgrade() -> None:
    op.drop_column('rentals', 'status')