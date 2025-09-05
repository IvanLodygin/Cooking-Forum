from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class PostAddForm(forms.ModelForm):
    """Форма для добавления новой статьи от пользователя"""
    
    class Meta:
        """Мета класс, указывающий поведенческий характер, чертеж для класса"""
        model = Post
        fields = ('title', 'content', 'photo', 'category')
        
        widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
   			'content': forms.Textarea(attrs={'class': 'form-control'}),
      		'photo': forms.FileInput(attrs={'class': 'form-control'}),
        	'category': forms.Select(attrs={'class': 'form-control'})
		}
        
class LoginForm(AuthenticationForm):
    """Форма для аутентификации пользователя"""
    username = forms.CharField(label='Имя пользователя', max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    password = forms.CharField(label='Пароль', max_length=150,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
class RegistrationForm(UserCreationForm):
    """Форма для регистрации пользователя"""
    
    class Meta:
        model = User
        
        fields = ('username', 'email', 'password1', 'password2')
        
    username = forms.CharField(max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Электронная почта'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Подтвердите пароль'}))
    
class CommentForm(forms.ModelForm):
    """Форма для написания комментария"""
    
    class Meta:
        model = Comment
        fields = ('text',)
        
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control',
                                          'placeholder': 'Текст вашего комментария'})
        }