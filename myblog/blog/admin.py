from django.contrib import admin
from .models import Post

'''
Displaying post on admin page.
    list_display: shown fields
    list_filters: fields to be filtered
    prepopulated_fields: slug field is filled automatically
'''
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
