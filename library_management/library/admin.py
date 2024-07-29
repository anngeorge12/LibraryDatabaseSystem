from django.contrib import admin
from library.models import Book, Borrow

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'available')
    search_fields = ('title', 'author', 'isbn')

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'return_date')
    search_fields = ('user__username', 'book__title')
