from django.shortcuts import render, redirect
from .models import Article, Contribution, Change
from .forms import ArticleForm, ContributeArticleForm
import difflib
from django.conf import settings



def articles_list(request):
	articles = Article.objects.all()
	context = {
		"articles" : articles,
	}
	return render(request, "articles_list.html", context)

def article_details(request, article_id):
	context = { "article" : Article.objects.get(id=article_id)}
	return render(request, "article_details.html", context)

def create_article(request):
	if request.user.is_anonymous:
		return redirect('login')    
	form = ArticleForm()
	if request.method == "POST":
		form = ArticleForm(request.POST)
		if form.is_valid():
			article = form.save(commit=False)
			article.author = request.user
			article.save()
			return redirect('article-details', article.id)

	context = {"form": form}

	return render(request, "create_article.html", context)

def edit_article(request, article_id):
	article = Article.objects.get(id=article_id)

	if article.author != request.user:
		return redirect('article-details', article_id)

	form = ArticleForm(instance=article)
	if request.method == "POST":
		form = ArticleForm(request.POST, instance=article)

		if form.is_valid():
			form.save()
			return redirect("article-details", article_id)

	context = {"form": form, "article": article}
	return render(request, "edit_article.html", context)

def my_articles_list(request):
	if request.user.is_anonymous:
		return redirect('login')
	return render(request, "my_articles_list.html")


def contribute_to_article(request, article_id):
	if request.user.is_anonymous:
		return redirect('login')
		
	article = Article.objects.get(id=article_id)
	
	#the author shouldn't be able to contribute, they can only edit
	if article.author == request.user:
		return redirect('edit-article', article_id)

	form = ContributeArticleForm(instance=article)
	if request.method == "POST":
		form = ContributeArticleForm(request.POST)

		if form.is_valid():
			changed_article = form.save(commit=False)
			contribution = Contribution.objects.create(user=request.user, article=article)
			Change.objects.create(new_content=changed_article.content, contribution=contribution)
			return redirect('my-contributions-list')

	context = {"form":form, "article":article}

	return render(request, 'contribute_to_article.html', context)

def my_contributions_list(request):
	if request.user.is_anonymous:
		return redirect('login')

	return render(request, "my_contributions_list.html")

def contributions_list(request):
	if request.user.is_anonymous:
		return redirect('articles-list')

	contributions = Contribution.objects.filter(status=Contribution.PENDING, article__author=request.user)
	context = {"contributions" : contributions}
	
	return render(request, 'contributions_list.html', context)

	# we were able to filter according to the author of the article (where article is a field in the Contribution model) 
	# by using __(double underscore) which allows us to get the value of one of the article's fields.


# import difflib

# string1 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
# Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
# Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
# """

# string2 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
# Unos aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
# """

# d = difflib.Differ()
# comparison = d.compare(string1.splitlines(), string2.splitlines())
# print(list(comparison))


def contribution_details(request, contribution_id):
	contribution = Contribution.objects.get(id=contribution_id)
	if request.user != contribution.article.author:
		return redirect('articles-list')

	d = difflib.Differ()
	comparison = list(d.compare(contribution.article.content.splitlines(True), contribution.change.new_content.splitlines(True)))

	context = {
		"contribution" : contribution,
		"comparison" : comparison,
	}
	
	return render(request, 'contribution_details.html', context)


def accept_changes(request, contribution_id):
	contribution = Contribution.objects.get(id=contribution_id)

	if request.user != contribution.article.author:
		return redirect('articles-list')
	
	contribution.status = Contribution.ACCEPTED
	contribution.save()

	article = contribution.article
	article.content = contribution.change.new_content
	article.save()

	contribution.change.delete()

	return redirect('contributions-list')

def decline_changes(request, contribution_id):
	contribution = Contribution.objects.get(id=contribution_id)

	if request.user != contribution.article.author :
		return redirect('articles-list')

	contribution.status = Contribution.DECLINED
	contribution.save()

	contribution.change.delete()

	return redirect('contributions-list')

def article_details(request, article_id):
	article = Article.objects.get(id=article_id)
	if settings.DEBUG:
		contributions = article.contributions.filter(status=Contribution.ACCEPTED)
	else:
		contributions = article.contributions.filter(status=Contribution.ACCEPTED).distinct('user')

	context = {
		"article": article,
		"contributions": contributions,
		}
	return render(request, "article_details.html", context)


