from django.contrib import admin

# Register your models here.
from .models import *

class EntryAdmin(admin.ModelAdmin):
    list_display = ('publication_date', 'author', 'title', 'slug')
    list_filter = ('publication_date', 'author')
    search_fields = ('author', 'title', 'body')
    prepopulated_fields = {'slug': ('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('entry', 'creation_date', 'author')
    list_filter = ('entry', 'creation_date', 'author')
    search_fields = ('entry', 'author', 'body')

admin.site.register(Entry, EntryAdmin)
admin.site.register(Comment, CommentAdmin)
