from django.shortcuts import render
from django.db import models
from django.db.models import Count
from .models import Article, Category, Tag, Comments, Advertisments
from django.contrib.auth.models import User
from random import randint
from django.utils import timezone
from datetime import timedelta

# Create your views here.

categories = Category.objects.annotate(popular=models.Count('article')).order_by('-popular')
popular_articles = Article.objects.order_by('-post_views')[:3]
top_articles = Article.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]

def advertisements():
    """
    Returns 3 random advertisements, all of different types, from the table of advertisements.
    """
    advertisements_square = Advertisments.objects.filter(banner_type = "square")
    square_index = randint(0, len(advertisements_square)-1)
    square = advertisements_square[square_index]

    advertisements_hor_rect = Advertisments.objects.filter(banner_type = "horizontal_rectangle")
    h_rect_index = randint(0, len(advertisements_hor_rect)-1)
    h_rect = advertisements_hor_rect[h_rect_index]


    advertisements_ver_rect = Advertisments.objects.filter(banner_type = "vertical_rectangle")
    v_rect_index = randint(0, len(advertisements_ver_rect)-1)
    v_rect = advertisements_ver_rect[v_rect_index]

    return (square,h_rect, v_rect)



def home(request):
    """
    Displayes the homepage of the site.
    """
    article_details = Article.objects.order_by('-created_at')
    article_header = Article.objects.order_by('-post_views')


    returned = {
        'categories': (categories.order_by('category_name'))[:5], 
        'article_header': article_header, 
        'article_details': article_details, 
        'popular_articles': popular_articles,
        'square': advertisements()[0],
        'h_rect': advertisements()[1],
        'v_rect': advertisements()[2],
        'top_articles': top_articles
    }
    
    return render(request, 'index.html', returned)

def details(request, pk):
    """
    Displays a webpage with all the details of a single article
    """
    article = Article.objects.filter(id = pk).first()
    article.post_views = article.post_views + 1
    article.save()

    previous_article = Article.objects.filter(id__lt = pk).order_by('-id').first()
    next_article = Article.objects.filter(id__gt = pk).order_by('id').first()

    category_articles = Article.objects.filter(category = article.category).order_by('-post_views')

    if request.method == "POST":
        if request.POST["name"] == "":
            name = "Anonymous"
        else:
            name = request.POST["name"]
        email = request.POST["email"]
        website = request.POST["website"]
        comment = request.POST["comment"]
        
        comment_add = Comments(name=name, email=email, website=website, comment=comment, article_id=pk)
        comment_add.save()

    comments = Comments.objects.filter(article_id = pk)
    comments_number = len(comments)

    current_date = timezone.now()

    returned = {
        'article': article, 
        'categories': categories[:5], 
        'popular_articles': popular_articles, 
        'previous_article': previous_article, 
        'next_article': next_article, 
        'category_articles': category_articles,
        'comments': comments,
        'comments_number': comments_number,
        'square': advertisements()[0],
        'h_rect': advertisements()[1],
        'v_rect': advertisements()[2],
        'top_articles': top_articles,
        'current_date': current_date
    }
    
    return render(request, 'single-article.html', returned)

def category(request, cat):
    """
    Displays all the articles under a specific category.
    """
    category_details = Category.objects.get(category_name = cat)
    category_articles = category_details.article_set.all()

    returned = {
        'square': advertisements()[0],
        'h_rect': advertisements()[1],
        'v_rect': advertisements()[2],
        'cat': cat, 
        'category_articles': category_articles, 
        'popular_articles': popular_articles, 
        'categories': categories[:5],
        'top_articles': top_articles
    }
    return render(request, 'category.html', returned)

def tags(request, tag):
    """
    Displays all the articles under a specific tag.
    """
    tag_details = Tag.objects.get(tag_name = tag)
    tag_articles = tag_details.article_set.all().order_by('post_views')

    returned = {
        'tag': tag, 
        'tag_articles': tag_articles, 
        'categories': categories[:5], 
        'popular_articles': popular_articles,
        'square': advertisements()[0],
        'h_rect': advertisements()[1],
        'v_rect': advertisements()[2],
    }

    return render(request, 'tag.html', returned)

def author(request, author):
    """
    Displays all the details of a specific author author
    """
    author_details = User.objects.get(id=author)
    author_articles = Article.objects.filter(author_id=author).order_by('-created_at')

    returned = {
        'square': advertisements()[0],
        'h_rect': advertisements()[1],
        'v_rect': advertisements()[2],
        'author_details': author_details, 
        'author_articles': author_articles, 
        'popular_articles': popular_articles, 
        'categories': categories[:5], 
        'top_articles': top_articles
    }
    return render(request, 'author.html', returned)
