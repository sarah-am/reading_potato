"""reading_potato URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views
from authentication import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('articles/', views.articles_list, name="articles-list"),
    path('articles/<int:article_id>/', views.article_details, name="article-details"),
    path('create/', views.create_article, name="create-article"),
    path('edit/<int:article_id>', views.edit_article, name="edit-article"),
    path('my-articles/', views.my_articles_list, name="my-articles-list"),

    path('register/', auth_views.register, name="register"),
]