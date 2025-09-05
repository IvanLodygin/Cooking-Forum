from django.urls import path
from .views import * # Импортируем все классы и функции из views.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('', index, name='index'), # За главную страничку отвечает функция index()
    path('category/<int:pk>/', category_list, name='category_list_link'), # category_list_link - уникальное имя ссылки
    path('post/<int:pk>/', post_detail, name='post_detail_link'),
    path('add_article/', add_post, name='add_link'),
    path('login/', user_login, name='login_link'),
    path('logout/', user_logout, name='logout_link'),
    path('register/', register, name='register_link'),
    path('add_comment/<int:post_id>', add_comment, name='add_comment_link'),
    path('profile/<int:user_id>', profile, name='profile_link'),
    
    path('post/<int:pk>/update/', PostUpdate.as_view(), name='update_post_link'),
    path('post<int:pk>/delete/', PostDelete.as_view(), name='post_delete_link'),
    path('search/', SearchResults.as_view(), name='search_link'),
    path('posts/api/', CookingAPI.as_view(), name='CookingAPI'),
    path('posts/api/<int:pk>/', CookingAPIDetail.as_view(), name='CookingAPIDetail'),
    path('categories/api/', CookingCategoryAPI.as_view(), name='CookingCategoryAPI'),
    path('categories/api/<int:pk>/', CookingCategoryAPIDetail.as_view(), name='CookingCategoryAPIDetail'),
    
    #API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify')
]
