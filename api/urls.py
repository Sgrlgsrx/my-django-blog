from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 创建路由器并注册视图集
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'profiles', views.ProfileViewSet, basename='profile')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'articles', views.ArticleViewSet, basename='article')
router.register(r'comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # DRF的登录登出
]

# API根视图
router.get_api_root_view().cls.__name__ = "BlogAPI"
router.get_api_root_view().cls.__doc__ = "博客系统REST API"