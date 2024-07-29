from ninja import NinjaAPI
from datetime import date
from library.models import Book, Borrow
from library.schemas import BookSchema, BookIn, BorrowSchema, BorrowIn
from ninja import Router
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from django.contrib.auth.models import User
from typing import List

api = NinjaAPI()


@api.get("/books", response=List[BookSchema])
def list_books(request):
    books = Book.objects.all()
    return books

admin_router = Router()

@admin_router.post("/books", response=BookSchema)
def add_book(request, book_in: BookIn):
    book = Book.objects.create(**book_in.dict())
    return book

@admin_router.put("/books/{book_id}", response=BookSchema)
def update_book(request, book_id: int, book_in: BookIn):
    book = get_object_or_404(Book, id=book_id)
    for attr, value in book_in.dict().items():
        setattr(book, attr, value)
    book.save()
    return book

@admin_router.delete("/books/{book_id}")
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return {"success": True}

api.add_router('/admin', admin_router)

user_router = Router()

@user_router.get("/books/available", response=List[BookSchema])
def list_available_books(request):
    books = Book.objects.filter(available=True)
    return books

@user_router.post("/borrow", response=BorrowSchema)
def borrow_book(request, data:BorrowIn):
    user = get_object_or_404(User, id=data.user_id)
    book = get_object_or_404(Book, id=data.book_id)
    if not book.available:
        raise HttpError(400, "Book is already borrowed")
    borrow = Borrow.objects.create(user=user, book=book)
    book.available = False
    book.save()
    return borrow

@user_router.post("/return", response=BorrowSchema)
def return_book(request, data:BorrowIn):
    borrow = get_object_or_404(Borrow, user_id=data.user_id, book_id=data.book_id, return_date__isnull=True)
    borrow.return_date = date.today()
    borrow.save()
    book = borrow.book
    book.available = True
    book.save()
    return borrow

api.add_router('/user', user_router)
