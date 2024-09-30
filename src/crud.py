from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from . import db
from . import schemas
from . import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_recipe(db: Session, top=10):
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


def get_or_create_recipe(db: Session, recipe: schemas.RecipeBase):
    existing_recipe = db.query(models.Recipe).filter_by(title=recipe.title).first()
    if existing_recipe:
        return existing_recipe
    else:
        return models.Recipe(
            title=recipe.title,
            description=recipe.description,
            instructions=recipe.instructions,
            image=recipe.image,
            ingredients=[
                get_or_create_ingredient(db, ing) for ing in recipe.ingredients
            ],
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


if __name__ == "__main__":
    session = db.SessionLocal()

    ingr1 = schemas.IngredientBase(
        title="flour", calories=10, image="flour.png", description="flour description"
    )
    ingr2 = schemas.IngredientBase(
        title="eggs", calories=100, image="eggs.png", description="egg description"
    )
    ingr3 = schemas.IngredientBase(
        title="nuttella",
        calories=1000,
        image="nuttella.png",
        description="nuttella description",
    )

    recipe1 = schemas.RecipeBase(
        title="Crepes",
        description="crepes description",
        ingredients=[ingr1, ingr2, ingr3],
        instructions="crepes instructions",
        image="crepes.png",
    )
    recipe2 = schemas.RecipeBase(
        title="Tagliatelle",
        description="Tagliatelle description",
        ingredients=[ingr1, ingr2],
        instructions="Tagliatelle instructions",
        image="taglietelle.png",
    )

    post_recipe(session, recipe1)
    post_recipe(session, recipe2)

    recipes = session.query(models.Recipe).all()
    for r in recipes:
        print(f"{r.title} has ingredients:")
        for i in r.ingredients:
            print(f"   - {i.title}")
