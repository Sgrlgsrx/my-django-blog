from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    """文章分类"""
    name = models.CharField(max_length=100, verbose_name='分类名称')
    description = models.TextField(blank=True, verbose_name='分类描述')
    
    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = '文章分类'
    
    def __str__(self):
        return self.name

class Article(models.Model):
    """文章模型"""
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
    )
    
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    excerpt = models.TextField(max_length=500, blank=True, verbose_name='摘要')
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='作者')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='分类')
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览量')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '文章'
        verbose_name_plural = '文章'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})
    
    def increase_views(self):
        """增加浏览量"""
        self.views += 1
        self.save(update_fields=['views'])