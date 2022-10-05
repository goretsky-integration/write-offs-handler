from pydantic import BaseModel, constr

__all__ = (
    'Ingredient',
    'IngredientIn',
)


class IngredientIn(BaseModel):
    name: constr(max_length=255, min_length=2)


class Ingredient(BaseModel):
    id: int
    name: str
