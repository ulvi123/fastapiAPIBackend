"""add content column to posts table

Revision ID: 5c857e62326e
Revises: cf248c146bac
Create Date: 2024-05-25 09:26:18.864124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c857e62326e'
down_revision: Union[str, None] = 'cf248c146bac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
