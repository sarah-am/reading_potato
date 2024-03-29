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
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('articles/', views.articles_list, name="articles-list"),
    path('articles/<article_slug>/', views.article_details, name="article-details"),
    path('create/', views.create_article, name="create-article"),
    path('edit/<article_slug>', views.edit_article, name="edit-article"),
    path('my-articles/', views.my_articles_list, name="my-articles-list"),

    path('register/', auth_views.register, name="register"),
    path('login/', auth_views.login_view , name="login"),
    path('logout/', auth_views.logout_view, name="logout"),

    path('contribute/<article_slug>/', views.contribute_to_article, name="contribute-to-article"),
    path('my-contributions/', views.my_contributions_list, name="my-contributions-list"),
    path('contributions/', views.contributions_list, name="contributions-list"),
    path('contributions/<int:contribution_id>/', views.contribution_details, name="contribution-details"),

    path('accept/<int:contribution_id>/', views.accept_changes, name="accept-changes"),
    path('decline/<int:contribution_id>/', views.decline_changes, name="decline-changes"),
]


urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
