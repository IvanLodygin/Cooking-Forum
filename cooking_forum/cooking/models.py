from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    # Категория новостей
    title = models.CharField(max_length=255, verbose_name='Название категории') # Поле символов с максимальной длиной, отображаемое имя в админке
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self): # Генерирование ссылки
        return reverse('category_list_link', kwargs={'pk': self.pk}) 
    
    
    class Meta: # Для корректного отображения в админке на русском языке
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
class Post(models.Model):
    # Для новостных постов
    title = models.CharField(max_length=255, verbose_name='Заголовок статьи')
    content = models.TextField(default='Скоро тут будет статья', verbose_name='Текст статьи') # default= наполнение по умолчанию
    created_at = models.DateTimeField(auto_now_add=True) # Привязка ко времени создания
    updated_at = models.DateTimeField(auto_now=True) # Привязка ко времени обновления
    photo = models.ImageField(upload_to='photos/', blank=True) # Фотографии статей будут скачиваться в каталог photos
    # blank = True - поле необязательно для заполнения; null = True - поле может быть пустым
    watched = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE) # Связываем класс с категорией, при удалении категории удаляются все статьи
    # related_name нужен для того, чтобы вызывать посты в ORM через category.posts
    author = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self): # Генерирование ссылки
        return reverse('post_detail_link', kwargs={'pk': self.pk}) 
    
    class Meta: # Для корректного отображения в админке на русском языке
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        
class Comment(models.Model):
    """Комментарии к постам"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'