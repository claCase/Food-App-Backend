"""create instruction table, update recipes and create recipe_instruction relations table

Revision ID: 2633a9db05c1
Revises: 6be0290203c6
Create Date: 2024-10-06 05:15:20.325167

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2633a9db05c1"
down_revision: Union[str, None] = "6be0290203c6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "instructions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("step_id", sa.Integer),
        sa.Column("instruction", sa.String),
    )

    op.create_table(
        "recipe_instructions",
        sa.Column("recipe_id", sa.Integer, sa.ForeignKey("recipes.id")),
        sa.Column("instruction_id", sa.Integer, sa.ForeignKey("instructions.id")),
        sa.UniqueConstraint(
            "recipe_id", "instruction_id", name="uix_recipe_instruction"
        ),
    )


def downgrade() -> None:
    op.drop_table("instructions")
    op.drop_table("recipe_instructions")
