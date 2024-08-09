import sqlite3
from fastapi import FastAPI
from db_models import database, users, products, orders
from db_models import UserIn, UserUpd, User
from db_models import ProductIn, ProductUpd, Product
from db_models import OrderIn, OrderUpd, Order
from datetime import datetime

app = FastAPI()

tables = {
        "users": users,
        "products": products,
        "orders": orders
    }


@app.get("/{table}/{item_id}/")
async def get_id_request(table: str, item_id: int):
    table_ = tables.get(table)
    if table_ is None:
        return {"message": f"Table {table} not found"}
    query = table_.select().where(table_.c.id == item_id)
    return await database.fetch_one(query)


@app.get("/{table}/")
async def get_all_request(table: str):
    table_ = tables.get(table)
    if table_ is None:
        return {"message": f"Table {table} not found"}
    query = table_.select()
    return await database.fetch_all(query)


@app.delete("/{table}/{item_id}")
async def delete_item(table: str, item_id: int):
    table_ = tables.get(table)
    if table_ is None:
        return {"message": f"Table {table} not found"}
    query = table_.delete().where(table_.c.id == item_id)
    await database.execute(query)
    return {"message": f"{table}[id={item_id}] has been deleted"}


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
    return await get_id_request("users", user_id)


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
    return await get_id_request("products", product_id)


@app.post("/orders/", response_model=Order)
async def create_order(new_order: OrderIn):
    query = orders.insert().values(order_date=datetime.now(),
                                   status="accepted",
                                   **new_order.dict())
    last_id = await database.execute(query)
    return await get_id_request("orders", last_id)


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, upd_order: OrderUpd):
    upd_order = upd_order.dict()
    upd_order = {k: v for k, v in upd_order.items() if v is not None}
    query = (orders.update().
             where(orders.c.id == order_id).
             values(**upd_order))
    await database.execute(query)
    return await get_id_request("orders", order_id)
