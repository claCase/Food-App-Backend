from typing import List, Optional
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    String,
    MetaData,
    Boolean,
    ForeignKey,
    Interval, 
    UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Mapped
from sqlalchemy.sql import text
from .db import Base, engine


# alembic: b6c44c3065c5
recipe_ingredients_association = Table(
    "recipe_ingredients",
    Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipes.id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id"), primary_key=True),
    UniqueConstraint("recipe_id", "ingredient_id", name="uix_recipe_ingredient"), 

)

# almebic: 2633a9db05c1 
recipe_instruction_association = Table(
    "recipe_instructions", 
    Base.metadata, 
    Column("recipe_id", Integer, ForeignKey("recepies.id"), primary_key=True),
    Column("instruction_id", Integer, ForeignKey("instructions.id"), primary_key=True),
    UniqueConstraint("recipe_id", "instruction_id", name="uix_recipe_instruction"), 

)

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, index=True)
    calories = Column(Integer)
    image = Column(String)
    description = Column(String)
    recipes = relationship(
        "Recipe", secondary=recipe_ingredients_association, back_populates="ingredients"
    )

class Instructions(Base):
    # almebic: 2633a9db05c1 
    __tablename__ = "instructions"

    id = Column(Integer, primary_key=True)
    step_id = Column(Integer)
    instruction = Column(String)
    recipe: Mapped["Recipe"] = relationship(
        "Recipe", secondary=recipe_instruction_association, back_populates="instructions"
    )


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, index=True)
    description = Column(String)
    instructions = Column(String)
    image = Column(String)
    duration = Column(Integer)
    ingredients = relationship(
        "Ingredient", secondary=recipe_ingredients_association, back_populates="recipes"
    )
    instructions: Mapped[List["Instructions"]] = relationship(
        "Instructions", secondary=recipe_instruction_association, back_populates="recipes"
    )
    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, unique=True, index=True)
    surname = Column(String, unique=True, index=True)
    age = Column(Integer, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


users_recipe_likes = Table(
    "user_likes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("recipe_id", Integer, ForeignKey("recipes.id")),
)

Base.metadata.create_all(engine)