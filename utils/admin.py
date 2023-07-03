from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(ContactUs)
class ContactAdmin(admin.ModelAdmin):
    list_display = [ "name",  "message", "ratings"]
    
    
@admin.register(BookTable)
class BookTableAdmin(admin.ModelAdmin):
    list_display = [ "name",  "number_of_persons", 'date', 'time']
    