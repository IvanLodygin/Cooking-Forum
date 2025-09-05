from django.contrib import admin
from .models import Category, Post, Comment

class PostAdmin(admin.ModelAdmin):
    # Вместо списков можно использовать кортежи, там, где это оптимально
    # Перечисляем, какие поля отображаются в админке в режиме предпросмотра
    list_display = ['id', 'title', 'watched', 'is_published', 'category', 'created_at', 'updated_at']
    # Перечисляем, какие поля кликабельные
    list_display_links = ['id', 'title']
    # Перечисляем, какие поля можно менять прямо в режиме предпросмотра
    list_editable = ['is_published']
    # Перечисляем, какие поля админ не может изменить
    readonly_fields = ['watched']
    # Перечисляем поля, по которым можно отфильтровать
    list_filter = ['is_published', 'category']

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)