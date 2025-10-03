from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),  # 所有文章相关路由
    path('users/', include('users.urls')),
    path('api/', include('api.urls')),
    path('', RedirectView.as_view(url='/articles/')),  # ✅ 首页重定向到文章列表
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)