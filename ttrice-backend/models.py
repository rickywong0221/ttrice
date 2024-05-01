from pydantic import computed_field, ValidationError, conint
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated, List, Optional
from annotated_types import Interval


# class Dish(BaseModel):
class Dish(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    wday: Annotated[int, Interval(ge=0, lt=6)]

    @computed_field
    def is_meat(self) -> bool:
        _meat_keywords: List[str] = ['牛', '豬', '雞', '魚', '羊', '叉燒', '肉', '班腩', '鴨', '鵝']
        for m in _meat_keywords:
            if m in self.name:
                return (True)
        return (False)


class Ricebox(SQLModel):
    FISH_SET_KEYWORD: str = '蒸倉魚'
    MAX_NO_OF_DISHES: int = 4
    MAX_NO_OF_FISH_DISHES: int = 3
    BASE_PRICE: int = 35
    PERDISH_PRICE: int = 8
    FISH_BASE_PRICE: int = 58
    dish1: Dish
    dish2: Dish

    # def __init__(self, d1, d2) -> None:
    #     if self.FISH_SET_KEYWORD in d1 or d2:
    #         self.price: int = self.FISH_BASE_PRICE
    #         self.max_dish: int = self.MAX_NO_OF_FISH_DISHES
    #     else:
    #         self.price: int = self.BASE_PRICE
    #         self.max_dish: int = self.MAX_NO_OF_DISHES
    #     self.dish_count: int = 2

    def __init__(self, d1, d2) -> None:
        self.price: int = 0
        self.dish_count: int = 0
        self.dish1 = d1
        self.dish2 = d2

    def add(self, dish: Dish):
        if len(self.dishes) < self.max_dish:
            self.dishes.append(dish)
            self.dish_count += 1
        else:
            raise ValueError(f"Your ricebox cannot have more than {self.max_dish} dishes")

    def __repr__(self):
        return str(self.dishes)
