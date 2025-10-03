from django.db import models
from django.contrib.auth.models import User
from articles.models import Article

class Comment(models.Model):
    """评论模型"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='文章')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论者')
    content = models.TextField(verbose_name='评论内容')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '评论'
        verbose_name_plural = '评论'
    
    def __str__(self):
        return f'{self.author.username} 对《{self.article.title}》的评论'