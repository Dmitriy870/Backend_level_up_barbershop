"""Initial migration

Revision ID: dc77997e49a7
Revises: 
Create Date: 2024-11-18 01:04:55.513267

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dc77997e49a7"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_user_id", table_name="user")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index("ix_user_id", "user", ["id"], unique=False)
    # ### end Alembic commands ###
