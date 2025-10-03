from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Article, Category
from comments.models import Comment

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        return Article.objects.filter(status='published').select_related('author', 'category')

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 获取最近文章
        context['recent_articles'] = Article.objects.filter(
            status='published'
        ).exclude(id=self.object.id)[:5]
        return context
    
    def get_object(self):
        obj = super().get_object()
        obj.increase_views()
        return obj

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'articles/article_form.html'
    fields = ['title', 'excerpt', 'content', 'category', 'status']
    success_url = reverse_lazy('articles:article-list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '文章发布成功！')
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    template_name = 'articles/article_form.html'
    fields = ['title', 'excerpt', 'content', 'category', 'status']
    
    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author
    
    def form_valid(self, form):
        messages.success(self.request, '文章更新成功！')
        return super().form_valid(form)

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'articles/article_confirm_delete.html'
    success_url = reverse_lazy('articles:article-list')
    
    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '文章删除成功！')
        return super().delete(request, *args, **kwargs)

# 新增评论处理函数
def post_comment(request, article_id):
    """处理评论提交"""
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        # 验证用户是否登录
        if not request.user.is_authenticated:
            messages.error(request, '请先登录再发表评论')
            return redirect('articles:article-detail', pk=article_id)
        
        # 获取评论内容
        content = request.POST.get('content', '').strip()
        
        # 基础验证
        if not content:
            messages.error(request, '评论内容不能为空')
        elif len(content) > 1000:
            messages.error(request, '评论内容不能超过1000字')
        else:
            # 创建评论
            Comment.objects.create(
                article=article,
                author=request.user,
                content=content
            )
            messages.success(request, '评论发布成功！')
    
    return redirect('articles:article-detail', pk=article_id)