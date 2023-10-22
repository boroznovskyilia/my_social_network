"""empty message

Revision ID: fe287baa26eb
Revises: 163a315b02e2
Create Date: 2023-09-15 19:15:02.509611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe287baa26eb'
down_revision: Union[str, None] = '163a315b02e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(None, 'post', 'user', ['username'], ['username'], ondelete='CASCADE',onupdate="CASCADE")


def downgrade() -> None:
    pass
