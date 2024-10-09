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
    UniqueConstraint,
    Date,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Mapped, mapped_column
from sqlalchemy.sql import text
from .db import Base, engine


recipe_tags_association = Table(
    "recipe_tags",
    Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipes.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
    UniqueConstraint("recipe_id", "tag_id", name="uix_recipe_tag"),
)

""" meals_tags_association = Table(
    "recipe_meals",
    Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipes.id"), primary_key=True),
    Column("meal_id", Integer, ForeignKey("meals.id"), primary_key=True),
    UniqueConstraint("recipe_id", "meal_id", name="uix_recipe_meal"),
)
 """


class RecipeIngredientAssociation(Base):
    __tablename__ = "recipe_ingredients"
    __table_args__ = (
        UniqueConstraint("recipe_id", "ingredient_id", name="uix_recipe_ingredient"),
    )

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    quantity = Column(String)
    unit = Column(String)

    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="recipe")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, index=True)
    calories = Column(Integer)
    image = Column(String)
    description = Column(String)
    recipe = relationship("RecipeIngredientAssociation", back_populates="ingredient")


class Instructions(Base):
    __tablename__ = "instructions"
    __table_args__ = (UniqueConstraint("recipe", "step_id", name="uix_recipe_step"),)
    id = Column(Integer, primary_key=True)
    step_id = Column(Integer, index=True)
    instruction = Column(String, index=True)
    recipe: Mapped[int] = mapped_column(ForeignKey("recipes.id"))


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, index=True)
    description = Column(String)
    ingredients = relationship("RecipeIngredientAssociation", back_populates="recipe")
    instructions: Mapped[List["Instructions"]] = relationship()
    tags: Mapped[List["Tag"]] = relationship(
        secondary=recipe_tags_association, back_populates="recipe"
    )
    image = Column(String)
    duration = Column(Integer)
    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id"))
    meal: Mapped[Optional["Meal"]] = relationship(back_populates="recipe")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    tag = Column(String, unique=True)
    recipe = relationship(
        "Recipe", secondary=recipe_tags_association, back_populates="tags"
    )


class Meal(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True)
    meal = Column(String, unique=True)
    recipe: Mapped["Recipe"] = relationship(back_populates="meal")


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", "name", "surname", name="uix_email_name_surname"),
    )
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    birthday = Column(Date, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


users_recipe_likes = Table(
    "user_likes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("recipe_id", Integer, ForeignKey("recipes.id")),
    UniqueConstraint("user_id", "recipe_id", name="uix_user_recipe"),
)

Base.metadata.create_all(engine)
