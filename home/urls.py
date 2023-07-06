from django.urls import path, include
from .views import home, details, category, tags, author, ArticleViewSet, AuthorViewSet, TagViewSet, CategoryViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet, basename="Article")
router.register(r'authors', AuthorViewSet, basename="Authors")
router.register(r'tags', TagViewSet, basename="Tags")
router.register(r'categories', CategoryViewSet, basename="Categories")

urlpatterns = [
    path('', home, name='home'),
    path('article/<int:pk>', details, name = 'article-detail'),
    path('category/<str:cat>', category, name = 'category'),
    path('tag/<str:tag>', tags, name = 'tag'),
    path('author/<int:author>', author, name = 'author'),
    path('api', include(router.urls)),
]