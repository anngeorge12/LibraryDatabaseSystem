from ninja import Schema
from pydantic import Field
from pydantic import BaseModel
from datetime import date

class BookSchema(Schema):
    id: int
    title: str
    author: str
    isbn: str
    available: bool

class BookIn(Schema):
    title: str
    author: str
    isbn: str

class BorrowSchema(Schema):
    id: int
    user_id: int
    book_id: int
    borrow_date: date
    return_date: date = None

class BorrowIn(BaseModel):
    user_id: int
    book_id: int

