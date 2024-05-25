"""Add user table

Revision ID: 89881ffedfee
Revises: 5c857e62326e
Create Date: 2024-05-25 09:31:14.049407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89881ffedfee'
down_revision: Union[str, None] = '5c857e62326e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                  sa.Column("id",sa.Integer(),nullable=False),
                  sa.Column("email",sa.String(),nullable=False), # type: ignore
                  sa.Column("password",sa.String(),nullable=False),
                  sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False),
                  sa.PrimaryKeyConstraint("id"),
                  sa.UniqueConstraint("email")
                )


def downgrade() -> None:
    op.drop_table("users")
