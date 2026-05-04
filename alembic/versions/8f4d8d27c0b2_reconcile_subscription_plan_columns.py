"""reconcile subscription_plans columns with current model

Revision ID: 8f4d8d27c0b2
Revises: 2b97e7d4c1a1
Create Date: 2026-04-24 00:00:01.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f4d8d27c0b2'
down_revision: Union[str, None] = '2b97e7d4c1a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _has_column(inspector: sa.Inspector, table_name: str, column_name: str) -> bool:
    return any(col['name'] == column_name for col in inspector.get_columns(table_name))


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    table_name = 'subscription_plans'

    if not _has_column(inspector, table_name, 'description'):
        op.add_column(table_name, sa.Column('description', sa.Text(), nullable=True))

    inspector = sa.inspect(bind)
    if not _has_column(inspector, table_name, 'duration_days'):
        op.add_column(
            table_name,
            sa.Column('duration_days', sa.Integer(), nullable=False, server_default='30'),
        )

    inspector = sa.inspect(bind)
    if not _has_column(inspector, table_name, 'max_books'):
        op.add_column(
            table_name,
            sa.Column('max_books', sa.Integer(), nullable=False, server_default='0'),
        )
        if _has_column(inspector, table_name, 'max_books_per_month'):
            op.execute(
                sa.text(
                    'UPDATE subscription_plans SET max_books = COALESCE(max_books_per_month, 0)'
                )
            )

    inspector = sa.inspect(bind)
    if not _has_column(inspector, table_name, 'price'):
        op.add_column(
            table_name,
            sa.Column('price', sa.Numeric(10, 2), nullable=False, server_default='0'),
        )
        if _has_column(inspector, table_name, 'price_per_month'):
            op.execute(
                sa.text('UPDATE subscription_plans SET price = COALESCE(price_per_month, 0)')
            )

    inspector = sa.inspect(bind)
    if not _has_column(inspector, table_name, 'max_magazines'):
        op.add_column(
            table_name,
            sa.Column('max_magazines', sa.Integer(), nullable=False, server_default='0'),
        )

    inspector = sa.inspect(bind)
    if not _has_column(inspector, table_name, 'created_at'):
        op.add_column(
            table_name,
            sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        )

    inspector = sa.inspect(bind)
    if not _has_column(inspector, table_name, 'updated_at'):
        op.add_column(
            table_name,
            sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        )

    op.execute(sa.text('UPDATE subscription_plans SET is_active = COALESCE(is_active, 1)'))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    table_name = 'subscription_plans'

    if _has_column(inspector, table_name, 'updated_at'):
        op.drop_column(table_name, 'updated_at')
    if _has_column(inspector, table_name, 'created_at'):
        op.drop_column(table_name, 'created_at')
    if _has_column(inspector, table_name, 'max_magazines'):
        op.drop_column(table_name, 'max_magazines')
    if _has_column(inspector, table_name, 'price'):
        op.drop_column(table_name, 'price')
    if _has_column(inspector, table_name, 'max_books'):
        op.drop_column(table_name, 'max_books')
    if _has_column(inspector, table_name, 'duration_days'):
        op.drop_column(table_name, 'duration_days')
    if _has_column(inspector, table_name, 'description'):
        op.drop_column(table_name, 'description')
