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


from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models

from ckeditor_uploader.widgets import CKEditorUploadingWidget

class FlatPageCustom(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget},
    }
    #fieldsets = (
#        (None, {'fields': ('url', 'title', 'content', 'sites')}),
#        (_('Advanced options'), {
#            'classes': ('collapse', ),
#            'fields': (
#                'enable_comments',
#                'registration_required',
#                'template_name',
#            ),
#        }),
#    )

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageCustom)
