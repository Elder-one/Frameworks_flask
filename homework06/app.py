import sqlite3
from typing import List
from fastapi import FastAPI
from homework06.db_models import database, users, products, orders
from homework06.db_models import UserIn, UserUpd, User
from homework06.db_models import ProductIn, ProductUpd, Product
from homework06.db_models import OrderIn, OrderUpd, Order
from datetime import datetime

app = FastAPI()


@app.get("/users/", response_model=List[User])
async def get_all_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.post("/users/")
async def create_user(new_user: UserIn):
    try:
        query = users.insert().values(**new_user.dict())
        last_id = await database.execute(query)
        return {"id": last_id, **new_user.dict()}
    except sqlite3.IntegrityError:
        return {"message": "Data does not fit the db requirements"}


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, upd_user: UserUpd):
    upd_user = upd_user.dict()
    upd_user = {k: v for k, v in upd_user.items() if v is not None}
    query = (users.update().
             where(users.c.id == user_id).
             values(**upd_user))
    await database.execute(query)
    return await get_user(user_id)


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {"message": f"User[id={user_id}] has been deleted"}


@app.get("/products/", response_model=List[Product])
async def get_all_products():
    query = products.select()
    return await database.fetch_all(query)


@app.get("/products/{product_id}", response_model=Product)
async def get_product(user_id: int):
    query = products.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.post("/products/", response_model=Product)
async def create_product(new_product: ProductIn):
    query = products.insert().values(**new_product.dict())
    last_id = await database.execute(query)
    return {"id": last_id, **new_product.dict()}


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, upd_product: ProductUpd):
    upd_product = upd_product.dict()
    upd_product = {k: v for k, v in upd_product.items() if v is not None}
    query = (products.update().
             where(products.c.id == product_id).
             values(**upd_product))
    await database.execute(query)
    return await get_product(product_id)


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = (products.delete().
             where(products.c.id == product_id))
    await database.execute(query)
    return {"message": f"Product[id={product_id}] has been deleted"}


@app.get("/orders/", response_model=List[Order])
async def get_all_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.post("/orders/", response_model=Order)
async def create_order(new_order: OrderIn):
    query = orders.insert().values(order_date=datetime.now(),
                                   status="accepted",
                                   **new_order.dict())
    last_id = await database.execute(query)
    return await get_order(last_id)


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, upd_order: OrderUpd):
    upd_order = upd_order.dict()
    upd_order = {k: v for k, v in upd_order.items() if v is not None}
    query = (orders.update().
             where(orders.c.id == order_id).
             values(**upd_order))
    await database.execute(query)
    return await get_order(order_id)


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = (orders.delete().
             where(orders.c.id == order_id))
    await database.execute(query)
    return {"message": f"Order[id={order_id}] has been deleted"}
