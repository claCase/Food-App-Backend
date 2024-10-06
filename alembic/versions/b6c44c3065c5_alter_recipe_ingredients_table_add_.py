"""alter recipe_ingredients table: add primary key constraint

Revision ID: b6c44c3065c5
Revises: 2633a9db05c1
Create Date: 2024-10-06 05:45:22.866988

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b6c44c3065c5"
down_revision: Union[str, None] = "2633a9db05c1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'new_recipe_ingredients',
        sa.Column('recipe_id', sa.Integer, sa.ForeignKey('recipes.id'), nullable=False),
        sa.Column('ingredient_id', sa.Integer, sa.ForeignKey('ingredients.id'), nullable=False),
        sa.UniqueConstraint('recipe_id', 'ingredient_id',  name="uix_recipe_ingredient"),  # Composite primary key
    )

    # Copy data from the old table to the new table
    op.execute("""
        INSERT INTO new_recipe_ingredients (recipe_id, ingredient_id)
        SELECT recipe_id, ingredient_id FROM recipe_ingredients
    """)

    # Drop the old table
    op.drop_table('recipe_ingredients')

    # Rename the new table to the old table's name
    op.rename_table('new_recipe_ingredients', 'recipe_ingredients')


def downgrade() -> None:
    # Recreate the old table structure without primary key constraints
    op.create_table(
        'old_recipe_ingredients',
        sa.Column('recipe_id', sa.Integer, sa.ForeignKey('recipes.id'), nullable=False),
        sa.Column('ingredient_id', sa.Integer, sa.ForeignKey('ingredients.id'), nullable=False),
        # Do not add any primary key constraints here
    )

    # Copy data back from the new table to the old table
    op.execute("""
        INSERT INTO old_recipe_ingredients (recipe_id, ingredient_id)
        SELECT recipe_id, ingredient_id FROM recipe_ingredients
    """)

    # Drop the new table
    op.drop_table('recipe_ingredients')

    # Rename the old table back to its original name
    op.rename_table('old_recipe_ingredients', 'recipe_ingredients')