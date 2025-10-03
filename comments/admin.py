from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'article__title', 'author__username']
    readonly_fields = ['created_at', 'updated_at']