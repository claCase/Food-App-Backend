from pydantic import BaseModel
from datetime import timedelta

class IngredientBase(BaseModel):
    title: str
    calories: int
    image: str
    description: str

class Instructions(BaseModel):
    step_id: int 
    instructions: str 

class RecipeBase(BaseModel):
    title: str
    description: str
    ingredients: list[IngredientBase]
    instructions: str
    image: str
    duration:int


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    name: str
    surname: str
    age: int


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
