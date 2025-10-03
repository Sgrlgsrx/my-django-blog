from rest_framework import serializers
from django.contrib.auth.models import User
from articles.models import Article, Category
from comments.models import Comment
from users.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['date_joined']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'location', 'website', 'avatar', 'created_at']
        read_only_fields = ['created_at']

class CategorySerializer(serializers.ModelSerializer):
    article_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'article_count']
    
    def get_article_count(self, obj):
        return obj.article_set.filter(status='published').count()

class ArticleListSerializer(serializers.ModelSerializer):
    """文章列表序列化器（简略信息）"""
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'excerpt', 'author', 'category', 
            'views', 'comment_count', 'created_at'
        ]
        read_only_fields = ['views', 'created_at']
    
    def get_comment_count(self, obj):
        return obj.comments.count()

class ArticleDetailSerializer(serializers.ModelSerializer):
    """文章详情序列化器（完整信息）"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'excerpt', 'author', 'category',
            'status', 'views', 'comments', 'created_at', 'updated_at'
        ]
        read_only_fields = ['views', 'created_at', 'updated_at']
    
    def get_comments(self, obj):
        comments = obj.comments.all()[:10]  # 只返回最近10条评论
        return CommentSerializer(comments, many=True).data

class ArticleCreateSerializer(serializers.ModelSerializer):
    """文章创建序列化器"""
    class Meta:
        model = Article
        fields = ['title', 'content', 'excerpt', 'category', 'status']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    """评论序列化器"""
    author = UserSerializer(read_only=True)
    article_title = serializers.CharField(source='article.title', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'article', 'article_title', 'author', 'content', 'created_at']
        read_only_fields = ['created_at']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)