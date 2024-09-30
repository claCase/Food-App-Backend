from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .db import SessionLocal, engine


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/recipe", response_model=schemas.RecipeBase)
def post_recipe(recipe: schemas.RecipeBase, db: Session = Depends(get_db)):
    db_recipe = crud.post_recipe(recipe=recipe, db=db)
    return db_recipe

@app.post("/ingredient", response_model=schemas.IngredientBase)
def post_recipe(ingredient: schemas.IngredientBase, db: Session = Depends(get_db)):
    db_ingredient = crud.post_ingredient(ingredient=ingredient, db=db)
    return db_ingredient 


@app.get("/recipe", response_model=list[schemas.RecipeBase])
def get_recipe(top: int = 10, db: Session = Depends(get_db)):
    recipes = crud.get_recipe(db=db, top=top)
    return recipes


@app.get("/recipe/{id}", response_model=schemas.RecipeBase)
def get_recipe_by_id(id: int, db: Session = Depends(get_db)):
    recipes = crud.get_recipe_by_id(recipe_id=id, db=db)
    return recipes


@app.get("/recipe/{name}", response_model=schemas.RecipeBase)
def get_recipe_by_name(name: str, db: Session = Depends(get_db)):
    recipes = crud.get_recipe_by_name(db=db, recipe_title=name)
    return recipes
