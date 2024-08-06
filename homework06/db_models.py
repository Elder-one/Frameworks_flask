import databases
from decimal import Decimal
import sqlalchemy as sa
from pydantic import BaseModel, Field, AfterValidator
from datetime import datetime
from typing import Optional, Annotated

DATABASE_URL = "sqlite:///database.db"

database = databases.Database(DATABASE_URL)
metadata = sa.MetaData()

users = sa.Table("users",
                 metadata,
                 sa.Column("id", sa.Integer, primary_key=True),
                 sa.Column("first_name", sa.String(64), nullable=False),
                 sa.Column("last_name", sa.String(64), nullable=False),
                 sa.Column("email", sa.String(100), nullable=False, unique=True),
                 sa.Column("password", sa.String(24), nullable=False))

products = sa.Table("products",
                    metadata,
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("product_name", sa.String(100), nullable=False),
                    sa.Column("description", sa.Text, nullable=False),
                    sa.Column("price", sa.DECIMAL(precision=2), nullable=False),
                    sa.CheckConstraint("price > 0", name="price_check"))

orders = sa.Table("orders",
                  metadata,
                  sa.Column("id", sa.Integer, primary_key=True),
                  sa.Column("user_id", sa.Integer,
                            sa.ForeignKey("users.id", ondelete="CASCADE"),
                            nullable=False),
                  sa.Column("product_id", sa.Integer,
                            sa.ForeignKey("products.id", ondelete="CASCADE"),
                            nullable=False),
                  sa.Column("order_date", sa.DateTime, nullable=False),
                  sa.Column("status", sa.String(15), nullable=False))

engine = sa.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

status_options = ["accepted", "in work", "closed"]


def one_of(value):
    assert value in status_options
    return value


class UserIn(BaseModel):
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    email: str = Field(max_length=100)
    password: str = Field(max_length=24)


class UserUpd(BaseModel):
    first_name: Optional[str] = Field(max_length=64)
    last_name: Optional[str] = Field(max_length=64)
    email: Optional[str] = Field(max_length=100)
    password: Optional[str] = Field(max_length=24)


class User(BaseModel):
    id: int
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    email: str = Field(max_length=100)
    password: str = Field(max_length=24)


class ProductIn(BaseModel):
    product_name: str = Field(max_length=100)
    description: str
    price: Decimal = Field(decimal_places=2, gt=0)


class ProductUpd(BaseModel):
    product_name: Optional[str] = Field(max_length=100)
    description: Optional[str]
    price: Optional[Decimal] = Field(decimal_places=2, gt=0)


class Product(BaseModel):
    id: int
    product_name: str = Field(max_length=100)
    description: str
    price: Decimal = Field(decimal_places=2, gt=0)


class OrderIn(BaseModel):
    user_id: int
    product_id: int


class OrderUpd(BaseModel):
    product_id: Optional[int]
    order_date: Optional[datetime]
    status: Annotated[str, AfterValidator(one_of)]


class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: datetime
    status: Annotated[str, AfterValidator(one_of)]
