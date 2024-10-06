from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from fastapi_pagination import add_pagination, Page
import uvicorn

from . import crud, models, schemas
from .db import SessionLocal, engine

from PIL import Image
import numpy as np 


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
def get_recipe(
    top: int = 10, db: Session = Depends(get_db)
):  # ->Page[schemas.RecipeBase]
    recipes = crud.get_recipe(db=db, top=top)
    return_recipes = []
    rid = np.random.choice(np.arange(top), size=top, replace=False).tolist()
    for id in rid:
        return_recipes.append(recipes[id])
    #print(type(recipes))
    #recipes = recipes[rid] 
    return return_recipes


@app.get("/recipe/{id}", response_model=schemas.RecipeBase)
def get_recipe_by_id(id: int, db: Session = Depends(get_db)):
    recipes = crud.get_recipe_by_id(recipe_id=id, db=db)
    return recipes


@app.get("/recipe/{name}", response_model=schemas.RecipeBase)
def get_recipe_by_name(name: str, db: Session = Depends(get_db)):
    recipes = crud.get_recipe_by_name(db=db, recipe_title=name)
    return recipes


@app.get("/image/{id}")
def get_image(id: str):
    try:
        return FileResponse(f"./images/{id}")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Image not found")


# add_pagination(app)
