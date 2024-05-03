"""
# Venturenix Lab: Advanced Generative AI: End to end development with LLMs
### Lession 2: Introduction to Python (2)

Goal: Rewrite the data models of thisthisrice using SQLModel and store the data on sqlite
"""

import re
from typing import Annotated, List, Optional, Dict
from annotated_types import Interval
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends
from models import Dish, Ricebox
from fastapi.middleware.cors import CORSMiddleware


# 定義環境及"constant"
CSV_FILE = 'thisthisrice.csv'
DB_PATH = 'rice.db'
SQLDB_PATH = 'sqlite:///' + DB_PATH


# Importing data
if Path(DB_PATH).exists():
    engine = create_engine(SQLDB_PATH)
    print("DB已建立，跳過CSV")
else:
    engine = create_engine(SQLDB_PATH)
    with open(CSV_FILE, 'r', encoding='utf-8') as file_descriptor:
        csv_content: list[str] = file_descriptor.readlines()
    # 移除最後一行
    csv_content.pop()
    pattern = re.compile(r"[0-9\. \n\*]+")
    fields_list: list[str] = []
    for line in csv_content:
        fields_list.append(line.split(","))
    # 問題1：*在這裡的用處；zip的功能
    dish_by_wday = list(zip(*fields_list))

    # 把Dish儲存到SQLite
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        for i in range(len(dish_by_wday)):
            for x in dish_by_wday[i]:
                session.add(Dish(name=pattern.sub('', x), wday=i))
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Greeting": "歡迎幫襯兩餸飯"}


@app.get("/menu/{wday}")
def read_item(wday: Annotated[int, Interval(ge=1, le=5)], session: Session = Depends(get_session)) -> List[Dish]:
    weekday = int(wday) - 1
    statement = select(Dish).where(Dish.wday == weekday)
    dishes = session.exec(statement).all()
    return(dishes)


@app.post("/create_ricebox")
def create_ricebox(dish1: str, dish2: str):
    Dish(name=dish1)
    ricebox = Ricebox(d1=dish1, d2=dish2)
    # ricebox = Ricebox(d1=dishes[0]["name"], d2=dishes[1]["name"])
    return {"message": f"你嘅飯盒而家有{ricebox.dish1}, {ricebox.dish2}"}

# @app.post("/dishes/", response_model=Ricebox)
# def add_dish(dish: Dish, ricebox: Ricebox):
#     dish_obj = Dish(**dish.dict())
#     ricebox.add(dish_obj)
#     return dish_obj






