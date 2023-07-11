from django.shortcuts import render
from django.db import models
from django.db.models import Count
from .models import Article, Category, Tag, Comments, Advertisments
from django.contrib.auth.models import User
from random import randint
from django.utils import timezone
from rest_framework import viewsets, filters
from .serializers import ArticleSerializer, AuthorSerializer, TagSerializer, CategorySerializer, CommentsSerializer, AdvertismentsSerializer
from rest_framework.pagination import LimitOffsetPagination
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


import googleapiclient.discovery

# Create your views here.

categories = Category.objects.annotate(popular=models.Count('article')).order_by('-popular')
popular_articles = Article.objects.order_by('-post_views')[:3]
top_articles = Article.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:3]

def youtube_videos():
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAxNgGrIAJotqa-pOA2A2XtulaUioZzeHk"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)

    api_request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId="UUE80xxtgnBxqb3DR6ThohvA",
        maxResults=3
    )

    response = api_request.execute()

    videos = response['items']

    return videos

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

    sidebar_videos = youtube_videos()

    returned = {
        'categories': (categories.order_by('category_name'))[:5], 
        'article_header': article_header, 
        'article_details': article_details, 
        'popular_articles': popular_articles,
        'square': advertisements()[0],
        'h_rect': advertisements()[1],
        'v_rect': advertisements()[2],
        'top_articles': top_articles,
        'sidebar_videos': sidebar_videos,
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
    sidebar_videos = youtube_videos()

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
        'current_date': current_date,
        'sidebar_videos': sidebar_videos,
    }
    
    return render(request, 'single-article.html', returned)

def category(request, cat):
    """
    Displays all the articles under a specific category.
    """
    category_details = Category.objects.get(category_name = cat)
    category_articles = category_details.article_set.all()
    sidebar_videos = youtube_videos()

    returned = {
        'square': advertisements()[0],
        'h_rect': advertisements()[1],
        'v_rect': advertisements()[2],
        'cat': cat, 
        'category_articles': category_articles, 
        'popular_articles': popular_articles, 
        'categories': categories[:5],
        'top_articles': top_articles,
        'sidebar_videos': sidebar_videos,
    }
    return render(request, 'category.html', returned)

def tags(request, tag):
    """
    Displays all the articles under a specific tag.
    """
    tag_details = Tag.objects.get(tag_name = tag)
    tag_articles = tag_details.article_set.all().order_by('post_views')
    sidebar_videos = youtube_videos()

    returned = {
        'tag': tag, 
        'tag_articles': tag_articles, 
        'categories': categories[:5], 
        'popular_articles': popular_articles,
        'square': advertisements()[0],
        'h_rect': advertisements()[1],
        'v_rect': advertisements()[2],
        'sidebar_videos': sidebar_videos,
    }

    return render(request, 'tag.html', returned)

def author(request, author):
    """
    Displays all the details of a specific author
    """
    author_details = User.objects.get(id=author)
    author_articles = Article.objects.filter(author_id=author).order_by('-created_at')
    sidebar_videos = youtube_videos()

    returned = {
        'square': advertisements()[0],
        'h_rect': advertisements()[1],
        'v_rect': advertisements()[2],
        'author_details': author_details, 
        'author_articles': author_articles, 
        'popular_articles': popular_articles, 
        'categories': categories[:5], 
        'top_articles': top_articles,
        'sidebar_videos': sidebar_videos,
    }
    return render(request, 'author.html', returned)

def videos(request):

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAxNgGrIAJotqa-pOA2A2XtulaUioZzeHk"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)

    api_request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId="UUE80xxtgnBxqb3DR6ThohvA",
        maxResults=50
    )

    response = api_request.execute()

    videos = response['items']
    sidebar_videos = videos[:3]

    paginator = Paginator(videos, 8)  # Number of videos per page
    page = request.GET.get('page')

    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        videos = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page
        videos = paginator.page(paginator.num_pages)

    returned = {
        'square': advertisements()[0],
        'h_rect': advertisements()[1],
        'v_rect': advertisements()[2],
        'popular_articles': popular_articles, 
        'categories': categories[:5], 
        'top_articles': top_articles,
        'videos': videos,
        'sidebar_videos': sidebar_videos,
    }

    return render(request, 'videos.html', returned)

class AuthorViewSet(viewsets.ModelViewSet):
    queryset =User.objects.all().order_by("first_name")
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name']
    pagination_class = LimitOffsetPagination

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("category_name")
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['category_name']
    pagination_class = LimitOffsetPagination

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by("tag_name")
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['tag_name']
    pagination_class = LimitOffsetPagination

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by("title")
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        author = User.objects.get(id=self.request.user.id)
        serializer.save(author=author)

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'id', 'category__category_name', 'tags__tag_name']
    pagination_class = LimitOffsetPagination

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all().order_by("name")
    serializer_class = CommentsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = LimitOffsetPagination

class AdvertisementsViewSet(viewsets.ModelViewSet):
    queryset = Advertisments.objects.all().order_by("alt")
    serializer_class = AdvertismentsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['alt']
    pagination_class = LimitOffsetPagination
   
