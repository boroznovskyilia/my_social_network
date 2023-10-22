"""empty message

Revision ID: 163a315b02e2
Revises: fdf9e5eb7fbc
Create Date: 2023-09-15 19:11:31.295204

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '163a315b02e2'
down_revision: Union[str, None] = 'fdf9e5eb7fbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(None, 'post', 'user', ['username'], ['username'], ondelete='CASCADE',onupdate="CASCADE")


def downgrade() -> None:
    pass
