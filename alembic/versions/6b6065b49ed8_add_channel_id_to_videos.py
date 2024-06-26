"""Add channel_id to videos

Revision ID: 6b6065b49ed8
Revises: 
Create Date: 2024-06-27 22:43:33.116444

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6b6065b49ed8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("videos", sa.Column("channel_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "videos", "channels", ["channel_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "videos", type_="foreignkey")
    op.drop_column("videos", "channel_id")
    # ### end Alembic commands ###
