from rest_framework import serializers
from .models import Article, User, Tag, Category

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'summary', 'image', 'content', 'category', 'tags']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag_name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name', 'category_details']