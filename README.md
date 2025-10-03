# Django Blog System

一个功能完整的博客系统，使用Django和Django REST Framework构建。

## ✨ 功能特性

- ✅ **用户系统** - 注册、登录、退出
- ✅ **文章管理** - 文章的增删改查（CRUD）
- ✅ **评论系统** - 文章评论功能
- ✅ **REST API** - 完整的API接口
- ✅ **管理后台** - Django Admin后台管理
- ✅ **响应式设计** - Bootstrap前端界面

## 🛠 技术栈

- **后端**: Django 4.2, Django REST Framework
- **数据库**: SQLite
- **前端**: Bootstrap 5, Django模板
- **认证**: Django内置认证系统

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Django 4.2

### 安装步骤
```bash
# 克隆项目
git clone <repository-url>

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 创建管理员
python manage.py createsuperuser

# 运行开发服务器
python manage.py runserver
```

### 访问地址
- 前端首页: http://localhost:8000/
- 管理后台: http://localhost:8000/admin/
- API接口: http://localhost:8000/api/

## 📁 项目结构
```
myblog_project/
├── articles/          # 文章管理
├── users/            # 用户管理
├── comments/         # 评论系统
├── api/              # REST API
├── templates/        # 前端模板
├── myblog/           # 项目配置
└── manage.py         # 管理脚本
```

## 🔧 核心功能

### 用户认证
- 用户注册、登录、退出
- 权限控制（用户只能管理自己的内容）
- 会话管理

### 文章系统
- 文章创建、编辑、删除
- 文章分类
- 浏览量统计
- 富文本内容

### REST API
```bash
GET    /api/articles/     # 获取文章列表
POST   /api/articles/     # 创建新文章
GET    /api/articles/1/   # 获取文章详情
PUT    /api/articles/1/   # 更新文章
DELETE /api/articles/1/   # 删除文章
```

## 👨‍💻 作者
**上官若离**
- 项目演示: [访问链接]
- 联系方式: [你的邮箱]

---

⭐ 如果这个项目对你有帮助，请给它一个Star！