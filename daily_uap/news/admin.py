from django.contrib import admin
from .models import Category, Post, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'is_published', 'published_date')
    list_filter = ('category', 'author', 'is_published', 'published_date')
    search_fields = ('title', 'content')
    list_editable = ('category', 'is_published')  # ✅ merged both editable fields
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('content',)
    ordering = ('-created_at',)
