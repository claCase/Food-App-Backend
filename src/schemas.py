from pydantic import BaseModel
from datetime import timedelta


class IngredientBase(BaseModel):
    title: str
    calories: int
    image: str
    description: str


class IngredientQuantity(BaseModel):
    ingredient: IngredientBase
    quantity: str
    unit: str


class InstructionsBase(BaseModel):
    step_id: int
    instruction: str


class TagsBase(BaseModel):
    tag: str


class MealBase(BaseModel):
    meal: str


class RecipeBase(BaseModel):
    title: str
    description: str
    instructions: list[InstructionsBase]
    ingredients: list[IngredientQuantity]
    tags: list[TagsBase]
    image: str
    duration: int
    meal: MealBase


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
