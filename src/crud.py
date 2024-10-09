from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import select
from . import db
from . import schemas
from . import models
from passlib.context import CryptContext

from fastapi_pagination.ext.sqlalchemy import paginate
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_recipe(db: Session, top=10):
    # return paginate(db, select(models.Recipe).limit(top))
    return db.query(models.Recipe).limit(top).all()


def get_recipe_by_id(db: Session, recipe_id: int):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()


def get_ingredient_by_id(db: Session, ingredient_id: int):
    return (
        db.query(models.Ingredient)
        .filter(models.Ingredient.id == ingredient_id)
        .first()
    )


def get_recipe_by_name(db: Session, recipe_title: str):
    return db.query(models.Recipe).filter(models.Recipe.title == recipe_title).first()


def get_ingredient_by_name(db: Session, ingredient_title: str):
    return (
        db.query(models.Ingredient)
        .filter(models.Ingredient.title == ingredient_title)
        .first()
    )


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        name=user.name,
        surname=user.surname,
        age=user.age,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_or_create_ingredient(db: Session, ingredient: schemas.IngredientBase):
    print(ingredient)
    existing_ingredient = (
        db.query(models.Ingredient).filter_by(title=ingredient.title).first()
    )
    if existing_ingredient:
        return existing_ingredient
    else:
        return models.Ingredient(
            title=ingredient.title,
            calories=ingredient.calories,
            image=ingredient.image,
            description=ingredient.description,
        )


def get_or_create_instruction(db: Session, instruction: schemas.InstructionsBase):
    existing_instruction = (
        db.query(models.Instructions)
        .filter_by(step_id=instruction.step_id, instruction=instruction.instruction)
        .first()
    )
    if existing_instruction:
        return existing_instruction
    else:
        return models.Instructions(
            step_id=instruction.step_id,
            instruction=instruction.instruction,
        )


def get_or_create_tags(db: Session, tags: schemas.TagsBase):
    existing_tag = db.query(models.Tag).filter_by(tag=tags.tag).first()
    if existing_tag:
        return existing_tag
    else:
        return models.Tag(tag=tags.tag)


def get_or_create_meal(db: Session, meal: schemas.MealBase):
    existing_meal = db.query(models.Meal).filter_by(meal=meal.meal).first()
    if existing_meal:
        return existing_meal
    else:
        return models.Meal(meal=meal.meal)


def get_or_create_recipe(db: Session, recipe: schemas.RecipeBase):
    existing_recipe = db.query(models.Recipe).filter_by(title=recipe.title).first()
    if existing_recipe:
        return existing_recipe
    else:
        return models.Recipe(
            title=recipe.title,
            description=recipe.description,
            instructions=[
                get_or_create_instruction(db, instruction)
                for instruction in recipe.instructions
            ],
            image=recipe.image,
            tags=[get_or_create_tags(db, tag) for tag in recipe.tags],
            duration=recipe.duration,
            meal=get_or_create_meal(db, recipe.meal),
        )


def post_recipe(db: Session, recipe: schemas.RecipeBase):
    db_recipe = get_or_create_recipe(db, recipe)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def post_ingredient(db: Session, ingredient: schemas.IngredientBase):
    db_ingredient = get_or_create_ingredient(db, ingredient)
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient


def add_recipe_with_ingredients(
    db,
    recipe: schemas.RecipeBase,
):
    db_recipe = post_recipe(db, recipe)

    for base_ingredient in recipe.ingredients:
        association = models.RecipeIngredientAssociation(
            recipe=db_recipe,
            ingredient=get_or_create_ingredient(db, base_ingredient.ingredient),
            quantity=base_ingredient.quantity,
            unit=base_ingredient.unit,
        )
        db.add(association)
    db.commit()


session = db.SessionLocal()

ingr1 = schemas.IngredientBase(
    title="whole chicken",
    description="1 (3½–4-lb.) whole chicken",
    image="1.jpg",
    calories=100,
)

ingr2 = schemas.IngredientBase(
    title="kosher salt",
    description="2¾ tsp. kosher salt, divided, plus more",
    image="1.jpg",
    calories=100,
)


ingrq1 = schemas.IngredientQuantity(ingredient=ingr1, quantity="2", unit="lb")
ingrq2 = schemas.IngredientQuantity(ingredient=ingr2, quantity="2¾", unit="tsp.")

instr1 = schemas.InstructionsBase(step_id=1, instruction="Add chicken")
instr2 = schemas.InstructionsBase(step_id=2, instruction="Add salt")
instr3 = schemas.InstructionsBase(step_id=3, instruction="Add pepper")

tag1 = schemas.TagsBase(tag="salty")
tag2 = schemas.TagsBase(tag="sour")

meal = schemas.MealBase(meal="dinner")

recipe1 = schemas.RecipeBase(
    title="Miso-Butter Roast Chicken With Acorn Squash Panzanella",
    description="Miso-Butter Roast Chicken With Acorn Squash Panzanella description",
    instructions=[instr1, instr2, instr3],
    ingredients=[ingrq1, ingrq2],
    tags=[tag1, tag2],
    image="2.jpg",
    duration=30,
    meal=meal,
)

add_recipe_with_ingredients(session, recipe1)


"""
from datetime import timedelta 

session = db.SessionLocal()
URI = "http://127.0.0.1:8000/"

ingr1 = schemas.IngredientBase(
    title="flour", calories=10, image=URI + "image/5.jpg", description="flour description"
)
ingr2 = schemas.IngredientBase(
    title="eggs", calories=100, image=URI + "image/4.jpg", description="egg description"
)
ingr3 = schemas.IngredientBase(
    title="nuttella",
    calories=1000,
    image= URI + "image/3.jpg",
    description="nuttella description",
)
ingr4 = schemas.IngredientBase(
    title="nuttella2",
    calories=1000,
    image= URI + "image/4.jpg",
    description="nuttella description",
)
ingr5 = schemas.IngredientBase(
    title="nuttella3",
    calories=1000,
    image= URI + "image/5.jpg",
    description="nuttella description",
)
ingr6 = schemas.IngredientBase(
    title="nuttella4",
    calories=1000,
    image= URI + "image/6.jpg",
    description="nuttella description",
)
ingr7 = schemas.IngredientBase(
    title="nuttella5",
    calories=1000,
    image= URI + "image/7.jpg",
    description="nuttella description",
)
ingr8 = schemas.IngredientBase(
    title="nuttella6",
    calories=1000,
    image= URI + "image/8.jpg",
    description="nuttella description",
)
ingr9  = schemas.IngredientBase(
    title="nuttella7",
    calories=1000,
    image= URI + "image/9.jpg",
    description="nuttella description",
)
ingr10 = schemas.IngredientBase(
    title="nuttella8",
    calories=1000,
    image= URI + "image/10.jpg",
    description="nuttella description",
)
ingr11 = schemas.IngredientBase(
    title="nuttella9",
    calories=1000,
    image= URI + "image/11.jpg",
    description="nuttella description",
)
ingr12 = schemas.IngredientBase(
    title="nuttella10",
    calories=1000,
    image= URI + "image/12.jpg",
    description="nuttella description",
)

recipe1 = schemas.RecipeBase(
    title="Crepes",
    description="crepes description",
    ingredients=[ingr1, ingr2, ingr3, ingr4, ingr5, ingr6, ingr7, ingr8, ingr9, ingr10, ingr11, ingr12],
    instructions="crepes instructions",
    image=URI + "image/1.jpg",
    duration=30
)
recipe2 = schemas.RecipeBase(
    title="Tagliatelle",
    description="Tagliatelle description",
    ingredients=[ingr1, ingr2, ingr3, ingr4, ingr5, ingr6, ingr7, ingr8, ingr9, ingr10, ingr11, ingr12],
    instructions="Tagliatelle instructions",
    image=URI + "image/2.jpg",
    duration=20
)
recipe3 = schemas.RecipeBase(
    title="Tagliatelle2",
    description="Tagliatelle description",
    ingredients=[ingr1, ingr2, ingr3, ingr4, ingr5, ingr6, ingr7, ingr8, ingr9, ingr10, ingr11, ingr12],
    instructions="Tagliatelle instructions",
    image=URI + "image/2.jpg",
    duration=20
)
recipe3 = schemas.RecipeBase(
    title="Crepes2",
    description="Tagliatelle description",
    ingredients=[ingr1, ingr2],
    instructions="Tagliatelle instructions",
    image=URI + "image/2.jpg",
    duration=20
)
recipe4 = schemas.RecipeBase(
    title="Crepes2",
    description="Tagliatelle description",
    ingredients=[ingr1, ingr2, ingr3],
    instructions="Tagliatelle instructions",
    image=URI + "image/2.jpg",
    duration=20
)
recipe5 = schemas.RecipeBase(
    title="Tagliatelle3",
    description="Tagliatelle description",
    ingredients=[ingr1, ingr2],
    instructions="Tagliatelle instructions",
    image=URI + "image/2.jpg",
    duration=20
)
recipe6 = schemas.RecipeBase(
    title="Tagliatelle4",
    description="Tagliatelle description",
    ingredients=[ingr1, ingr2],
    instructions="Tagliatelle instructions",
    image=URI + "image/2.jpg",
    duration=20
)
recipe7 = schemas.RecipeBase(
    title="Tagliatelle5",
    description="Tagliatelle description",
    ingredients=[ingr1, ingr2],
    instructions="Tagliatelle instructions",
    image=URI + "image/2.jpg",
    duration=20
)
recipe8 = schemas.RecipeBase(
    title="Tagliatelle6",
    description="Tagliatelle description",
    ingredients=[ingr1, ingr2],
    instructions="Tagliatelle instructions",
    image=URI + "image/2.jpg",
    duration=20
)
recipe9 = schemas.RecipeBase(
    title="Tagliatelle7",
    description="Tagliatelle description",
    ingredients=[ingr1, ingr2],
    instructions="Tagliatelle instructions",
    image=URI + "image/2.jpg",
    duration=20
)
recipe10 = schemas.RecipeBase(
    title="Tagliatelle8",
    description="Tagliatelle description",
    ingredients=[ingr1, ingr2],
    instructions="Tagliatelle instructions",
    image=URI + "image/2.jpg",
    duration=20
)
recipe11 = schemas.RecipeBase(
    title="Tagliatelle9",
    description="Tagliatelle description",
    ingredients=[ingr1, ingr2],
    instructions="Tagliatelle instructions",
    image=URI + "image/2.jpg",
    duration=20
)
recipe12 = schemas.RecipeBase(
    title="Tagliatelle10",
    description="Tagliatelle description",
    ingredients=[ingr1, ingr2, ingr3],
    instructions="Tagliatelle instructions",
    image=URI + "image/2.jpg",
    duration=20
)
recipe13 = schemas.RecipeBase(
    title="Tagliatelle11",
    description="Tagliatelle description",
    ingredients=[ingr1, ingr3],
    instructions="Tagliatelle instructions",
    image=URI + "image/2.jpg",
    duration=20
)

post_recipe(session, recipe1)
post_recipe(session, recipe2)
post_recipe(session, recipe3)
post_recipe(session, recipe4)
post_recipe(session, recipe5)
post_recipe(session, recipe6)
post_recipe(session, recipe7)
post_recipe(session, recipe8)
post_recipe(session, recipe8)
post_recipe(session, recipe10)
post_recipe(session, recipe11)
post_recipe(session, recipe12)
post_recipe(session, recipe13)

recipes = session.query(models.Recipe).all()
for r in recipes:
    print(f"{r.title} has ingredients:")
    for i in r.ingredients:
        print(f"   - {i.title}")
"""
