from django.shortcuts import render, redirect
from .models import Category, Post, Comment
from django.db.models import F, Q
from .forms import PostAddForm, LoginForm, RegistrationForm, CommentForm
from django.contrib.auth import login, logout
from django.views.generic import ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .serializers import PostSerializer, CategorySerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

def index(request):
    """Для главной странички"""
    posts = Post.objects.all() # Делаем ORM запрос в БД через модельки, получаем все объекты Post
    categrories = Category.objects.all()
    
    context = {
      'title': 'Главная страница',
      'posts': posts,
      'categories': categrories
	  } # Формируем данные, которые будем отправлять
    
    # Рендерим html страничку
    return render(request, 'cooking/index.html', context) ### Отправляем данные на html страничку, которую надо прогрузить

# Пример написания на базе класса
class Index(ListView):
  """Для главной странички"""
  model = Post
  context_object_name = 'posts'
  template_name = 'cooking/index.html'
  extra_context = {'title': 'Главная страница'}
  
def category_list(request, pk):
  """Реакция на нажатие кнопки категории"""
  posts = Post.objects.filter(category_id=pk)
  categrories = Category.objects.all()

  context = {
      'title': posts[0].category,
      'posts': posts,
      'categories': categrories
	} # Формируем данные, которые будем отправлять
    
  return render(request, 'cooking/index.html', context) ### Отправляем данные на html страничку, которую надо прогрузить

def post_detail(request, pk):
  """Страница статьи"""
  article = Post.objects.get(pk=pk)
  Post.objects.filter(pk=pk).update(watched=F('watched') + 1)
  ext_posts = Post.objects.all().exclude(pk=pk).order_by('-watched')[:5]
  comments = Comment.objects.filter(post=article)
     
  context = {
    'title': article.title,
    'post': article,
    'ext_posts': ext_posts,
    'comments': comments
  }
  
  if(request.user.is_authenticated):
    context['comment_form'] = CommentForm
  
  return render(request, 'cooking/article_detail.html', context)

def add_post(request):
  """Добавление статьи пользователя без админки"""
  
  if request.method == 'POST':
    form = PostAddForm(request.POST, request.FILES)
    
    if(form.is_valid()):
      post = form.save(commit=False)
      # Устанавливаем автора
      post.author = request.user
      # Теперь сохраняем
      post.save()
      return redirect('post_detail_link', post.pk)
  else:
    form = PostAddForm()
    
  context = {
    'form': form,
    'title': 'Добавить статью'
  }
  
  return render(request, 'cooking/article_add_form.html', context)

def user_login(request):
  """Аутентификация пользователя"""
  
  if(request.method == 'POST'):
    form = LoginForm(data=request.POST)
    
    if(form.is_valid()):
      user = form.get_user()
      login(request, user)
      
    return redirect('index')
  
  else:
    form = LoginForm()
    
  context = {
    'title': 'Авторизация пользователя',
    'form': form
  }
  
  return render(request, 'cooking/login_form.html', context)

def user_logout(request):
  '''Выход пользователя'''
  logout(request)
  
  return redirect('index')

def register(request):
  """Регистрация пользователя"""
  
  if(request.method == 'POST'):
    form = RegistrationForm(data=request.POST)
    
    if(form.is_valid()):
      form.save()
      return redirect('login_link')
  else:
    form = RegistrationForm()
  
  context = {
    'title': 'Регистрация пользователя',
    'form': form
  }
  
  return render(request, 'cooking/register.html', context)

class PostUpdate(UpdateView):
  '''Изменение статьи по кнопке'''
  model = Post
  form_class = PostAddForm
  template_name = 'cooking/article_add_form.html'
  
class PostDelete(DeleteView):
  """Удаление поста по кнопке"""
  model = Post
  success_url = reverse_lazy('index')
  context_object_name = 'post'
  
class SearchResults(Index):
  """Поиск-слово в заголовках и содержаниях статьи"""
  
  def get_queryset(self):
    word = self.request.GET.get('q')
    posts = Post.objects.filter(
      Q(title__icontains=word) | Q(content__icontains=word)
    )
    return posts
  
def add_comment(request, post_id):
  '''Добавление комментария к статье'''
  form = CommentForm(data=request.POST)
  
  if(form.is_valid()):
    comment = form.save(commit=False)
    comment.user = request.user
    comment.post = Post.objects.get(pk=post_id)
    comment.save()
  
  return redirect('post_detail_link', post_id)

def profile(request, user_id):
  '''Страница пользователя'''
  
  user = User.objects.get(pk=user_id)
  posts = Post.objects.filter(author=user)
  
  context = {
    'user': user,
    'posts': posts
  }
  
  return render(request, 'cooking/profile.html', context)

class CookingAPI(ListAPIView):
  """Выдача всей статей по API"""
  queryset = Post.objects.filter(is_published=True)
  serializer_class = PostSerializer
  
class CookingAPIDetail(RetrieveAPIView):
  """Выдача статьи по API"""
  queryset = Post.objects.filter(is_published=True)
  serializer_class = PostSerializer
  permission_classes = (IsAuthenticated,)
  
class CookingCategoryAPI(ListAPIView):
  """Выдача всей статей по API"""
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  
class CookingCategoryAPIDetail(RetrieveAPIView):
  """Выдача статьи по API"""
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  