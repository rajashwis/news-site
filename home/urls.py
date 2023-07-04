from django.urls import path
from .views import home, details, category, tags, author

urlpatterns = [
    path('', home, name='home'),
    path('article/<int:pk>', details, name = 'article-detail'),
    path('category/<str:cat>', category, name = 'category'),
    path('tag/<str:tag>', tags, name = 'tag'),
    path('author/<int:author>', author, name = 'author'),
]