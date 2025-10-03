from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from articles.models import Article, Category
from comments.models import Comment
from users.models import Profile
from .serializers import (
    UserSerializer, ProfileSerializer, CategorySerializer,
    ArticleListSerializer, ArticleDetailSerializer, ArticleCreateSerializer,
    CommentSerializer
)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """用户API（只读）"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """用户资料API（只读）"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """分类API（只读）"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ArticleViewSet(viewsets.ModelViewSet):
    """文章API"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Article.objects.filter(status='published').select_related('author', 'category')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action == 'create':
            return ArticleCreateSerializer
        else:
            return ArticleDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """增加文章浏览量"""
        article = self.get_object()
        article.increase_views()
        return Response({'views': article.views})
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """获取文章的所有评论"""
        article = self.get_object()
        comments = article.comments.all()
        page = self.paginate_queryset(comments)
        
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    """评论API"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Comment.objects.all()
        article_id = self.request.query_params.get('article')
        if article_id:
            queryset = queryset.filter(article_id=article_id)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)