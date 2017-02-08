from django.contrib import admin

# Register your models here.
from .models import book,Author

admin.site.register(book)
admin.site.register(Author)
