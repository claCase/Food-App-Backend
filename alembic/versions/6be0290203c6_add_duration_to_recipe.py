"""add duration to recipe

Revision ID: 6be0290203c6
Revises: 
Create Date: 2024-10-01 04:52:36.999174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta


# revision identifiers, used by Alembic.
revision: str = '6be0290203c6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.add_column("recipes", sa.Column("duration", sa.Integer()))
    connection = op.get_bind()
    connection.execute(
        sa.text("UPDATE recipes SET duration = :duration"), 
        {"duration":30}
    )

def downgrade() -> None:
    op.drop_column("recipes", "duration")